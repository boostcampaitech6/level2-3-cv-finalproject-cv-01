from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime

import exchange_calendars as ecals

from database import connection

from utils import logical_date, update_stock_query


default_args = {
    "owner": "sihyun",
    "depends_on_past": False, 
    "start_date": datetime(2024, 3, 27),
    'retries': 3,  
    'retry_delay': timedelta(minutes=5) 
}

def validation(date):
    date = logical_date(date)
    print(f"========== Execution date is {date} ==========")

    XKRX = ecals.get_calendar("XKRX")
    if XKRX.is_session(date):
        return "update_stock_task"
    
    return "close_date"

def update_stock(date):
    date = logical_date(date)

    kospi_df = fdr.StockListing('KOSPI')
    kosdaq_df = fdr.StockListing('KOSDAQ')

    korea_stock_df = pd.concat([kospi_df, kosdaq_df])
    korea_stock_symbol = korea_stock_df[['Code', 'Name','Market']]

    result = []

    for _,stock in korea_stock_symbol.iterrows():
        code, name, market = stock['Code'], stock['Name'], stock['Market']

        df = fdr.DataReader(code,'2024',date)

        if len(df) < 40 or str(df.index[-1]).split(' ')[0] != date: # 모델이 추론 불가능한 데이터 -> 추가 안함
            continue 
        else:
            row_data = [ code, name, market, date ]
            result.append(row_data)

    # 데이터 베이스 갱신
    update_query = update_stock_query()

    with connection.cursor() as cursor:
        for data in result:
            cursor.execute(update_query, data)

    connection.commit()
    connection.close()


with DAG(
    dag_id="update_stock_db",
    default_args=default_args,
    schedule_interval="0 10 * * *", 
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

    update_stock_task = PythonOperator(
        task_id="update_stock_task",
        python_callable=update_stock,
        op_kwargs={
            'date': execution_date,
        }
    )

    valid_check_task >> [update_stock_task, close_date]

