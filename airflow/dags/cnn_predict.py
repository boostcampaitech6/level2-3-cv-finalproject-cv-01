from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator


from datetime import datetime

import exchange_calendars as ecals
import FinanceDataReader as fdr

from cnn_model import rasterize, inference
from database import connection

from utils import get_stock_table, cnn_pred_query, logical_date

default_args = {
    "owner": "sihyun",
    "depends_on_past": False, 
    "start_date": datetime(2024, 3, 27),
    'retries': 3,  
    'retry_delay': timedelta(minutes=10) 
}


def validation(date):
    date = logical_date(date)

    print(f"========== Execution date is {date} ==========")

    XKRX = ecals.get_calendar("XKRX")
    if XKRX.is_session(date):
        return "predict_task"
    return "close_date"


def predict(date):
    date = logical_date(date)

    stock_table = get_stock_table(connection, date)

    datetime_date = datetime.strptime(date,'%Y-%m-%d')
    result = []
    for dic in stock_table:
        code = dic['stock_code']
        close = fdr.DataReader(code, date, date).iloc[0]['Close']
        
        stock_image = rasterize(code, datetime_date)
        preds = inference(stock_image)

        preds_result = [code,datetime_date,close]

        for idx, pct in preds:
            preds_result.extend([idx, pct])

        result.append(preds_result)

    cnn_insert_query = cnn_pred_query()
    with connection.cursor() as cursor:
        for row_data in result:
            cursor.execute(cnn_insert_query, row_data)

    connection.commit()
    connection.close()
        

with DAG(
    dag_id="cnn_predict",
    default_args=default_args,
    schedule_interval="0 11 * * *", 
    tags=['Single-run DAG'],
) as dag:
    execution_date = "{{ ds }}"

    close_date = EmptyOperator(task_id="close_date")

    valid_check_task = BranchPythonOperator(
        task_id="valid_check_task",
        python_callable=validation,
        op_kwargs={
            'date': execution_date,
        }
    )

    predict_task = PythonOperator(
        task_id="predict_task",
        python_callable=predict,
        op_kwargs={
            'date': execution_date,
        }
    )

    valid_check_task >> [predict_task, close_date]

