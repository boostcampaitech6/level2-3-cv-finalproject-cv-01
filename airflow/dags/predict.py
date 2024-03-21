from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

import os
import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime
from dateutil.relativedelta import relativedelta

import exchange_calendars as ecals

from model import rasterize, inference
from database import connection

# V1 

default_args = {
    "owner": "sihyun",
    "depends_on_past": False, 
    "start_date": datetime(2024, 3, 18),
    'retries': 3,  
    'retry_delay': timedelta(minutes=10) 
}

def validation(date):
    ks_date = date

    XKRX = ecals.get_calendar("XKRX")
    if XKRX.is_session(ks_date):
        return "predict_task"
    
    return "end"

def predict(date):
    ks_date = date

    with connection.cursor() as cursor:
        query = "SELECT * FROM ForTest2"
        cursor.execute(query)
        stock_table = cursor.fetchall()

    columns = [
        "stock_code",
        "date",
        "pred_1day_result",
        "pred_1day_percent",
        "pred_2day_result",
        "pred_2day_percent",
        "pred_3day_result",
        "pred_3day_percent",
        "pred_4day_result",
        "pred_4day_percent",
        "pred_5day_result",
        "pred_5day_percent",
        "pred_6day_result",
        "pred_6day_percent",
        "pred_7day_result",
        "pred_7day_percent"
    ]
    primary_key_columns = ["stock_code", "date"]
    update_clause = ", ".join([f"{column} = VALUES({column})" for column in columns if column not in primary_key_columns])

    results = []

    for dic in stock_table:
        
        code = dic['Code']

        close_price = fdr.DataReader(code, ks_date, ks_date).iloc[0]['Close']
        stock_image = rasterize(code, ks_date)
        preds = inference(stock_image)

        preds_result = [code,ks_date]

        for idx, pct in preds:
            preds_result.extend([idx, pct])

        with connection.cursor() as cursor:
            # 서비스 전 임시로 사용하는 cnnpredhistory 테이블에 모델 예측 결과들 저장
            query = f"INSERT INTO cnnpredhistory ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))}) ON DUPLICATE KEY UPDATE {update_clause}"
            cursor.execute(query, preds_result)

    connection.commit()


with DAG(
    dag_id="cnn_predict_db",
    default_args=default_args,
    schedule_interval="0 14 * * *", 
    tags=['my_dags'],
) as dag:
    execution_date = "{{ ds }}"

    end = EmptyOperator(task_id="end")

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

    valid_check_task >> [predict_task, end]

