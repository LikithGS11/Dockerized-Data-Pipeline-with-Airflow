from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Add scripts directory to path
sys.path.append('/opt/airflow/scripts')

from fetch_stock_data import fetch_and_store_stock_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'stock_pipeline',
    default_args=default_args,
    description='A simple stock data pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

fetch_stock_data_task = PythonOperator(
    task_id='fetch_stock_data',
    python_callable=fetch_and_store_stock_data,
    dag=dag,
)
