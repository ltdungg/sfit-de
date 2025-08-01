from airflow.sdk import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
from crawler import TikiCrawler
import datetime

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': datetime.timedelta(minutes=5),
    'start_date': datetime.datetime(2025, 7, 12)
}

@dag(
    'get_prices_per_four_hour',
    default_args=default_args,
    schedule='0 */4 * * *',
    max_active_runs=1,
    tags=['tiki', 'prices'],
    description='Fetch and store product prices from Tiki every 4 hours',
    catchup=False,
)
def get_prices_per_four_hour():

    @task
    def fetch_and_store_prices():
        tiki_crawler = TikiCrawler()

        products = tiki_crawler.get_all_products()

        if not products:
            print("No products found.")
            return
        print(f"Total products fetched: {len(products)}")
        # Convert products to DataFrame
        df = pd.DataFrame(products)

        return df

    @task
    def store_prices_to_db(df: pd.DataFrame):
        if df.empty:
            print("No data to store.")
            return

        pg_hook = PostgresHook(postgres_conn_id='tiki_db')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Insert data into the table
        for _, row in df.iterrows():
            insert_query = """
            INSERT INTO prices (product_id, current_price, original_price, discount_rate, quantity_sold, rating_average, review_count, crawled_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (row['product_id'], row['price'], row['original_price'], row['discount_rate'], row['quantity_sold'], row['rating_average'], row['review_count'], row['crawled_timestamp']))

        conn.commit()
        cursor.close()
        conn.close()

    fetched_data = fetch_and_store_prices()
    fetched_data >> store_prices_to_db(fetched_data)

get_prices_per_four_hour()