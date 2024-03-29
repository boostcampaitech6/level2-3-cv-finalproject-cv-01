from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

import os
import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime
from dateutil.relativedelta import relativedelta

# from stock_utils import valid_check
import exchange_calendars as ecals

from database import connection

default_args = {
    "owner": "sihyun",
    "depends_on_past": False, 
    "start_date": datetime(2024, 3, 17),
    'retries': 3,  
    'retry_delay': timedelta(minutes=5) 
}

def validation(date):
    ks_date = date
    XKRX = ecals.get_calendar("XKRX")
    if XKRX.is_session(ks_date):
        return "update_stock_task"
    
    return "end"

def update_stock(date):
    # db 전체 삭제
    krx_table = 'ForTest2' # 서비스전 임시로 저장되는 주가 종목 테이블 이름

    with connection.cursor() as cursor:
        query = f"DELETE FROM {krx_table}"
        cursor.execute(query)
        connection.commit()
    
    ks_date = date

    kospi_df = fdr.StockListing('KOSPI')
    kosdaq_df = fdr.StockListing('KOSDAQ')

    korea_stock_df = pd.concat([kospi_df, kosdaq_df])
    korea_stock_symbol = korea_stock_df[['Code', 'Name','Market']]
    korea_stock_symbol

    # 주가 종목에서 길이가 40 이하인건 저장안하게 하기
    rmv_list = []
    for _,stock in korea_stock_symbol.iterrows():
        stock_code = stock['Code']

        if len(fdr.DataReader(stock_code)) < 40:
            rmv_list.append(stock_code)

    krx_df = korea_stock_symbol[~korea_stock_symbol['Code'].isin(rmv_list)]

    with connection.cursor() as cursor:
        for _, row in krx_df.iterrows():
            code, name, market = row['Code'], row['Name'], row['Market']
            query = f"INSERT INTO {krx_table} (Code, Name, Market) VALUES (%s, %s, %s)"
            values = (code, name, market)
            cursor.execute(query, values)
        connection.commit() 


with DAG(
    dag_id="renew_stock_db",
    default_args=default_args,
    schedule_interval="0 12 * * *", 
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

    update_stock_task = PythonOperator(
        task_id="update_stock_task",
        python_callable=update_stock,
        op_kwargs={
            'date': execution_date,
        }
    )

    valid_check_task >> [update_stock_task, end]

