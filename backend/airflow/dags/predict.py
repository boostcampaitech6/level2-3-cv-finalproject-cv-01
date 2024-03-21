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

# V1 

default_args = {
    "owner": "sihyun",
    "depends_on_past": False, 
    "start_date": datetime(2024, 3, 7),
    'retries': 3,  
    'retry_delay': timedelta(minutes=10) 
}

def validation(date):
    # ks_date = datetime.strptime(date,'%Y-%m-%d')
    # ks_date = ks_date + relativedelta(days=1)
    # ks_date = ks_date.strftime("%Y-%m-%d")
    ks_date = date

    XKRX = ecals.get_calendar("XKRX")
    if XKRX.is_session(ks_date):
        return "predict_task"
    
    return "end"

def predict(date):
    # ks_date = datetime.strptime(date,'%Y-%m-%d')
    # ks_date = ks_date + relativedelta(days=1)
    # ks_date = ks_date.strftime("%Y-%m-%d")
    ks_date = date


    # 주식 코드 db 테이블에서 반복문으로 각 코드 가져오기
    file_name = f'./dags/database/symbol_data/korea_stock_symbols_{ks_date}.csv'
    stock_table = pd.read_csv(file_name)

    column = ['Date', 'Name', 'Code', 'Close_Price', \
                'Day_1', 'Day_2', 'Day_3', 'Day_4', 'Day_5', 'Day_6', 'Day_7']
    predict_df = pd.DataFrame(columns=column)

    for _, stock in stock_table.iterrows():
        
        code = stock['value'].split(':')[1]
        name = stock['label']

        close_price = fdr.DataReader(code, ks_date, ks_date).iloc[0]['Close']
        stock_image = rasterize(code, ks_date)
        preds = inference(stock_image)
        preds_result = []
        for idx, pct in preds:
            preds_result.append(str(idx)+'/'+str(round(pct,2)))
        
        result = [ks_date, name, code, close_price]
        result.extend(preds_result)

        predict_df = pd.concat([predict_df, pd.DataFrame([result],columns=column)])

    save_dir = './dags/database/predict_table'
    predict_df.to_csv(os.path.join(save_dir, f"predict_{ks_date}.csv"))

    

with DAG(
    dag_id="cnn_predict",
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

