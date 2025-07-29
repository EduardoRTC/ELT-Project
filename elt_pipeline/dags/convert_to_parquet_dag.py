# dags/convert_to_parquet_via_job.py
from datetime import datetime
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator

# ⇩  mantenha como inteiro, sem aspas
DATABRICKS_JOB_ID: int = 796193440724625

with DAG(
    dag_id="convert_to_parquet_via_job",
    start_date=datetime(2025, 7, 30),
    schedule=None,          # gatilho manual por enquanto
    catchup=False,
    tags=["databricks", "elt"],
) as dag:

    trigger_convert_job = DatabricksRunNowOperator(
        task_id="trigger_convert_job",
        databricks_conn_id="databricks_default",  # host + token do mesmo workspace
        job_id=DATABRICKS_JOB_ID,                 # ← agora é inteiro
        notebook_params={
            # se seu Job tiver widgets/params, declare-os aqui
            # "input_path": "/Volumes/…/landing/rel_vendas.xlsx",
        },
    )
