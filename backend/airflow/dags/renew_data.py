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

default_args = {
    "owner": "sihyun",
    "depends_on_past": False, 
    "start_date": datetime(2024, 3, 7),
    'retries': 3,  
    'retry_delay': timedelta(minutes=5) 
}

def validation(date):
    # ks_date = datetime.strptime(date,'%Y-%m-%d')
    # ks_date = ks_date + relativedelta(days=1)
    # ks_date = ks_date.strftime("%Y-%m-%d")
    ks_date = date

    XKRX = ecals.get_calendar("XKRX")
    if XKRX.is_session(ks_date):
        return "update_stock_task"
    
    return "end"

def update_stock(date):
    # ks_date = datetime.strptime(date,'%Y-%m-%d')
    # ks_date = ks_date + relativedelta(days=1)
    # ks_date = ks_date.strftime("%Y-%m-%d")
    ks_date = date

    # 자동 완성을 위한 주가 코드 테이블 갱신
    folder_name = './dags/database/symbol_data'
    file_name = f'korea_stock_symbols_{ks_date}.csv'
    file_path = os.path.join(folder_name, file_name)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    kospi_list = fdr.StockListing('KOSPI')
    kosdaq_list = fdr.StockListing('KOSDAQ')

    korea_stock_list = pd.concat([kospi_list, kosdaq_list])

    korea_stock_symbol = korea_stock_list[['Code', 'Name']]

    code_list, name_list = [], []

    for _, stock in korea_stock_symbol.iterrows():
        code = stock['Code']
        name = stock['Name']

        if len(fdr.DataReader(code)) < 40 or date not in fdr.DataReader(code).index:
            continue
        code_list.append(code)
        name_list.append(name)

    korea_stock_df = pd.DataFrame({'Code': code_list, 'Name' : name_list})
    korea_stock_df['Code'] = 'KRX:' + korea_stock_df['Code']

    korea_stock_df.rename(columns={'Name': 'label', 'Code': 'value'}, inplace=True)
    korea_stock_df.to_csv(file_path, index=False, encoding='utf-8-sig')




with DAG(
    dag_id="renew_stock_data",
    default_args=default_args,
    schedule_interval="0 13 * * *", 
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

