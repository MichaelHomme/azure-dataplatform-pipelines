from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator


default_args = {
    "owner": "data_engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dbt_kubernetes_pipeline",
    default_args=default_args,
    description="Runs dbt in Kubernetes using image from Azure Container Registry",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["dbt", "kubernetes", "acr"],
) as dag:
    run_dbt = KubernetesPodOperator(
        task_id="run_dbt",
        name="run-dbt",
        namespace="airflow",  # must be airflow, not default
        service_account_name="airflow-worker",
        image="acrixgs8i.azurecr.io/dbt:latest",
        image_pull_policy="Always",
        is_delete_operator_pod=False,
        in_cluster=True,
        get_logs=True,
        cmds=["bash", "-c"],
        arguments=[
            "dbt seed",
            "dbt run"
        ],
        on_finish_action="keep_pod",
    )
