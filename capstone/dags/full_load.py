"""
DAG: tiki_full_load_v3.py
Apache Airflow >=3.0 – Task SDK (3-task ETL)
Place file in $AIRFLOW_HOME/dags/
"""

from __future__ import annotations
import logging
from typing import List, Dict

import pendulum
import pandas as pd
from psycopg2.extras import execute_values

from airflow.sdk import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Local crawler module
from crawler import TikiCrawler  # noqa: E402

PRODUCT_COLUMNS: list[str] = [
    "product_id",
    "sku",
    "product_name",
    "category",
    "product_url",
    "thumbnail_url",
]
PRICE_COLUMNS: list[str] = [
    "product_id",
    "price",
    "original_price",
    "discount_rate",
    "quantity_sold",
    "rating_average",
    "review_count",
    "crawled_at",
]


@task()
def extract_products() -> List[Dict]:
    """
    Call TikiCrawler and return raw product list.
    """
    logger = logging.getLogger("airflow.task")
    crawler = TikiCrawler()
    raw_products = crawler.get_all_products()
    logger.info("Extracted %s raw products", len(raw_products))
    return raw_products  # XCom via pickling (Python object)


@task()
def transform_products(raw_records: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Transform raw list into two cleaned tables: products & prices.
    Returns dict with two lists of dicts to keep XCom lightweight.
    """
    logger = logging.getLogger("airflow.task")
    df_raw = pd.DataFrame(raw_records)

    # Products
    df_products = (
        df_raw.rename(
            columns={
                "name": "product_name",
                "url_path": "product_url",
                "prime_category_name": "category",
            }
        )
        .loc[:, PRODUCT_COLUMNS]
        .dropna(subset=["product_id"])
        .drop_duplicates(subset=["product_id"], keep="last")
    )

    # Prices
    df_prices = (
        df_raw.rename(columns={"crawled_timestamp": "crawled_at"})
        .loc[:, PRICE_COLUMNS]
        .dropna(subset=["product_id"])
    )
    numeric_cols = [
        "price",
        "original_price",
        "discount_rate",
        "quantity_sold",
        "rating_average",
        "review_count",
    ]
    df_prices[numeric_cols] = df_prices[numeric_cols].apply(
        pd.to_numeric, errors="coerce"
    )

    logger.info(
        "Transform done: %s products, %s price rows",
        len(df_products),
        len(df_prices),
    )

    # Convert to list[dict] to reduce serialization size
    return {
        "products": df_products.to_dict(orient="records"),
        "prices": df_prices.to_dict(orient="records"),
    }


@task()
def load_to_postgres(data: Dict[str, List[Dict]]) -> None:
    """
    Load products (upsert) and prices (append) into Postgres.
    """
    logger = logging.getLogger("airflow.task")
    pg_hook = PostgresHook(postgres_conn_id="tiki_db")
    with pg_hook.get_conn() as conn:
        with conn.cursor() as cur:
            # Upsert products
            product_query = """
                INSERT INTO products (
                    product_id, sku, product_name, category,
                    product_url, thumbnail_url
                )
                VALUES %s
                ON CONFLICT (product_id) DO UPDATE SET
                    sku=EXCLUDED.sku,
                    product_name=EXCLUDED.product_name,
                    category=EXCLUDED.category,
                    product_url=EXCLUDED.product_url,
                    thumbnail_url=EXCLUDED.thumbnail_url,
                    updated_at=NOW();
            """
            execute_values(
                cur,
                product_query,
                [[p[c] for c in PRODUCT_COLUMNS] for p in data["products"]],
                page_size=1000,
            )
            # Insert prices
            price_query = """
                INSERT INTO prices (
                    product_id, current_price, original_price, discount_rate,
                    quantity_sold, rating_average, review_count, crawled_at
                )
                VALUES %s;
            """
            execute_values(
                cur,
                price_query,
                [[p[c] for c in PRICE_COLUMNS] for p in data["prices"]],
                page_size=1000,
            )
        conn.commit()
    logger.info(
        "Load completed: %s products upserted, %s price rows inserted",
        len(data["products"]),
        len(data["prices"]),
    )


@dag(
    dag_id="tiki_full_load_v1",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Ho_Chi_Minh"),
    schedule=None,  # Manual trigger
    catchup=False,
    tags=["tiki", "full_load", "postgres"],
)
def tiki_full_load_pipeline():
    """
    Full-load Tiki product catalog & price history into Postgres.
    """
    raw = extract_products()
    transformed = transform_products(raw)
    load_to_postgres(transformed)


tiki_full_load_dag = tiki_full_load_pipeline()
