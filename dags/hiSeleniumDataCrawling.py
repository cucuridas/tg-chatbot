from ast import operator
from airflow.models.baseoperator import BaseOperator
from airflow import DAG
from datetime import datetime, timedelta
from operators.login_operator import LoginOperator

from sqlalchemy import desc
with DAG(
    dag_id='hiSeleniumDataCrawling',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1)
    },
    description="DAG for data crawling hiworks board",
    schedule_interval=timedelta(days=1),
    start_date=datetime(datetime.now().year, datetime.now().month, datetime.now().day),
    catchup=False,
    tags=['data import'],
) as dag:
    t1 = LoginOperator(
        task_id='login_task'
    )