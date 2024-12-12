from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

# Supposed to run every minute
with DAG(dag_id="post_pusher", start_date=datetime(2022, 1, 1), schedule="* * * * *", catchup=False) as dag:
    entry = BashOperator(task_id="hello", bash_command="python3 main.py --one")
