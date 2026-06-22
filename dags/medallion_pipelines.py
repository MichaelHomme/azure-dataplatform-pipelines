from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime, timedelta
import pendulum
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

    # Step 1: Load the raw CSVs into Postgres (Bronze)
    dbt_seed = KubernetesPodOperator(
        task_id='dbt_seed_raw_data',
        name='dbt-seed',
        namespace='airflow',
        image='ghcr.io/dbt-labs/dbt-postgres:1.7.latest',
        cmds=["dbt", "seed", "--profiles-dir", "/opt/airflow/dbt", "--project-dir", "/opt/airflow/dbt"],
        # Pulls the password we injected into AKS earlier!
        env_vars={'DBT_PASSWORD': dbt_password,
                  'DBT_USER': dbt_user},
        is_delete_operator_pod=True,
        in_cluster=True,
        get_logs=True,
    )

    # Step 2: Run the Medallion transformations (Silver & Gold)
    dbt_run = KubernetesPodOperator(
        task_id='dbt_run_models',
        name='dbt-run',
        namespace='airflow',
        image='ghcr.io/dbt-labs/dbt-postgres:1.7.latest',
        cmds=["dbt", "run", "--profiles-dir", "/opt/airflow/dbt", "--project-dir", "/opt/airflow/dbt"],
        env_vars={'DBT_PASSWORD': dbt_password,
                  'DBT_USER': dbt_user},
        is_delete_operator_pod=True,
        in_cluster=True,
        get_logs=True,
    )

    # Define the dependency (Seed first, then Run)
    dbt_seed >> dbt_run