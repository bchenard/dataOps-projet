from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

# Supposed to run every minute
with DAG(dag_id="post_pusher", start_date=datetime(2022, 1, 1), schedule="* * * * *", catchup=False) as dag:
    run_script = KubernetesPodOperator(
        task_id='run_post_pusher',
        name='post-pusher',
        namespace='projet',
        image='2024_kubernetes_post_pusher',
        image_pull_policy='Never',
        is_delete_operator_pod=True,
        is_paused_upon_creation=False
    )
