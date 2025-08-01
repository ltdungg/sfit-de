import datetime
from airflow.sdk import dag, task
from airflow.providers.standard.operators.empty import EmptyOperator


@dag(
    start_date=datetime.datetime(2021, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["example"]
)
def my_sample_dag():
    @task
    def generate_random_number():
        import random
        number = random.randint(1, 100)
        print(f"Generated number: {number}")
        return number

    @task
    def process_number(number):
        result = number * 2
        print(f"Processed number: {result}")
        return result

    # Định nghĩa dependencies
    num = generate_random_number()
    process_number(num)


# Khởi tạo DAG
my_sample_dag()
