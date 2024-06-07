from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fetch_fbi_data',
    default_args=default_args,
    description='A DAG to fetch FBI wanted data',
schedule_interval=timedelta(hours=1),
    start_date=days_ago(1),
    tags=['fbi', 'data'],
)

fetch_data = DockerOperator(
    task_id='fetch_fbi_data',
    image='data_fetching_service:latest',
    api_version='auto',
    auto_remove=True,
    command="python fetch_fbi_data.py",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    dag=dag,
)

fetch_data
