from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.sdk import Variable

# Normal call style
dbt_user = Variable.get("DBT_USER")
dbt_password = Variable.get("DBT_PASSWORD")

default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dbt_medallion_pipeline',
    default_args=default_args,
    description='Runs the dbt Medallion Architecture (Bronze -> Silver -> Gold)',
    schedule='@daily', # <--- CHANGED FROM schedule_interval
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    # test bashoperator
    test_bash = BashOperator(
        task_id='test_bash',
        bash_command='echo "Hello, World!"',
    )

    # List files in Pod
    list_files = BashOperator(
        task_id='list_files',
        bash_command='ls -l /opt/airflow',
    )

test_bash >> list_files
