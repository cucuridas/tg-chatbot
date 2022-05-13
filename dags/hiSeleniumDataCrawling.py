from ast import operator
from airflow.models.baseoperator import BaseOperator
from airflow import DAG
from datetime import datetime, timedelta

from sqlalchemy import desc
with DAG(
    'hiSeleniumDataCrawling',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    description="DAG for data crawling hiworks' board",
    schedule_interval=timedelta(days=1),
    start_date=datetime(datetime.now().year, datetime.now().month, datetime.now().day),
    catchup=False,
    tags=['data import'],
) as dag:
    t1 = BaseOperator(
        task_id='crawling'
    )
    t2 = BaseOperator(
        task_id='writing'
    )
    
t1 >> t2