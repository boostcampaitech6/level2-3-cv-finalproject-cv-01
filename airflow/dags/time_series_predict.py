from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator


from datetime import datetime

import FinanceDataReader as fdr
import exchange_calendars as ecals

from ts_model import ar_stock_prediction, lstm_model, lstm_inference , HMM
from database import connection
from utils import get_stock_table, ts_pred_query, logical_date



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
        return "ar_task"
    
    return "close_date"

def ar_predict(date):
    date = logical_date(date)

    stock_table = get_stock_table(connection, date)

    result = []

    for row in stock_table:
        code = row['stock_code']
        close = fdr.DataReader(code, date, date).iloc[0]['Close']

        # AR Model
        ar_pred = ar_stock_prediction(code,date)
        if ar_pred != None:
            ar_row_data = [code, date, close, "ar"]
            ar_row_data.extend(ar_pred)
            result.append(ar_row_data)
        

    insert_query = ts_pred_query()
    with connection.cursor() as cursor: 
        for row_data in result:
            cursor.execute(insert_query, row_data)

    connection.commit()
    print("AR Predict Successed")


def hmm_predict(date):
    date = logical_date(date)

    stock_table = get_stock_table(connection, date)

    result = []

    for row in stock_table:
        code = row['stock_code']
        close = fdr.DataReader(code, date, date).iloc[0]['Close']

        hmm_model = HMM(code, date)
        hmm_preds = hmm_model.forecast()
        hmm_row_data = [code, date, close, "hmm"]
        hmm_row_data.extend(hmm_preds)
        result.append(hmm_row_data)
        
        
    insert_query = ts_pred_query()
    with connection.cursor() as cursor: 
        for row_data in result:
            cursor.execute(insert_query, row_data)

    connection.commit()
    connection.close()
    print("HMM Predict Successed")

def lstm_predict(date):
    date = logical_date(date)

    stock_table = get_stock_table(connection, date)

    result = []
    model = lstm_model()

    for row in stock_table:
        code = row['stock_code']
        close = fdr.DataReader(code, date, date).iloc[0]['Close']

         # LSTM
        lstm_row_data = [code, date, close, "lstm"]
        preds = lstm_inference(model, code, date)
        lstm_row_data.extend(preds)
        result.append(lstm_row_data)

        
    insert_query = ts_pred_query()
    with connection.cursor() as cursor: 
        for row_data in result:
            cursor.execute(insert_query, row_data)

    connection.commit()
    print("LSTM Predict Successed")
    

with DAG(
    dag_id="time_series_predict",
    default_args=default_args,
    schedule_interval="30 13 * * *", 
    tags=['Single-run DAG'],
) as dag:
    execution_date = "{{ ds }}"

    close = EmptyOperator(task_id="close_date")

    valid_check_task = BranchPythonOperator(
        task_id="valid_check_task",
        python_callable=validation,
        op_kwargs={
            'date': execution_date,
        }
    )

    ar_task = PythonOperator(
        task_id="ar_task",
        python_callable=ar_predict,
        op_kwargs={
            'date': execution_date,
        }
    )

    hmm_task = PythonOperator(
        task_id="hmm_task",
        python_callable=hmm_predict,
        op_kwargs={
            'date': execution_date,
        }
    )

    lstm_task = PythonOperator(
        task_id="lstm_task",
        python_callable=lstm_predict,
        op_kwargs={
            'date': execution_date,
        }
    )

    valid_check_task >> [ar_task, close]
    ar_task >> lstm_task >> hmm_task
