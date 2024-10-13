from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from datetime import timedelta
from src.insertData import insertJsonData, insertCsvData, createIndex, createTable

defaultArguments = {
    "owner": "Felix Pratamasan",
    "start_date": days_ago(1),
    "retries": 1,
    "retry_delay": timedelta(hours=1)
}

dag = DAG(
    "Get_All_LLM_Data",
    default_args = defaultArguments,
    schedule_interval = "0 0 * * *",
    description = "Insert all llm data into MongoDB"
)

createTable = PythonOperator(
    task_id= "create_table",
    python_callable= createTable,
    dag = dag
)
insertJson = PythonOperator(
    task_id= "get_json_data",
    python_callable=insertJsonData,
    dag=dag
)

insertCsv = PythonOperator(
    task_id= "get_csv_data",
    python_callable=insertCsvData,
    dag=dag
)

ingestData = PythonOperator(
    task_id = "ingest_data",
    python_callable = createIndex,
    dag=dag
)

createTable>> insertJson >> insertCsv >> ingestData