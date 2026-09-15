from datetime import datetime, timedelta
import os
import sys

# Добавляем корень проекта в пути поиска модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.extract import run_extract
from src.transform import run_transform
from src.dq import run_dq_checks
from src.load import run_load

default_args = {
    "owner": "student",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="etl_variant_02",
    default_args=default_args,
    description="End-to-end Weather ETL Pipeline",
    schedule_interval=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="extract",
        python_callable=run_extract,
        op_kwargs={"execution_date": "{{ ds }}"},
    )

    t2 = PythonOperator(
        task_id="transform",
        python_callable=run_transform,
        op_kwargs={"execution_date": "{{ ds }}"},
    )

    t3 = PythonOperator(
        task_id="dq_checks",
        python_callable=run_dq_checks,
        op_kwargs={"execution_date": "{{ ds }}"},
    )

    t4 = PythonOperator(
        task_id="load",
        python_callable=run_load,
        op_kwargs={"execution_date": "{{ ds }}"},
    )

    t1 >> t2 >> t3 >> t4
