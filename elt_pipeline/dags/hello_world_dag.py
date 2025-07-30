from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def hello_world():
    print("Hello World from Airflow!")
    print("Esta é minha primeira DAG funcionando!")
    return "Sucesso"

# Configurações padrão
default_args = {
    'owner': 'estudante',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Criando a DAG
dag = DAG(
    'hello_world',
    default_args=default_args,
    description='Minha primeira DAG - Hello World',
    schedule_interval='@daily',
    catchup=False,
    tags=['exemplo', 'hello-world']
)

# Task 1: Comando bash
task_bash = BashOperator(
    task_id='print_date',
    bash_command='echo "Data atual: $(date)"',
    dag=dag
)

# Task 2: Função Python
task_python = PythonOperator(
    task_id='hello_world_python',
    python_callable=hello_world,
    dag=dag
)

# Task 3: Outro comando bash
task_final = BashOperator(
    task_id='say_goodbye',
    bash_command='echo "Goodbye from Airflow!"',
    dag=dag
)

# Definindo dependências
task_bash >> task_python >> task_final