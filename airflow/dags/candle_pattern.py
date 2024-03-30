from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

from datetime import datetime

from pattern_match import get_stock_data, cleanPx, detect_candle_patterns
from utils import get_stock_table, pattern_match_query
import exchange_calendars as ecals

from database import connection

from utils import logical_date

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
        return "predict_task"
    return "close_date"

def predict(date):
    date = logical_date(date)

    stock_table = get_stock_table(connection, date)

    result = []

    for dic in stock_table:
        code = dic["stock_code"]

        stock = get_stock_data(code, date)
        stock = cleanPx(stock)
        stock = detect_candle_patterns(stock)

        last_valid_index = stock['candlestick_pattern'].last_valid_index()

        if last_valid_index is not None:
            last_date = stock.iloc[last_valid_index]['Date']
            last_pattern = stock.loc[last_valid_index, 'candlestick_pattern']
            row_data = [code, last_date, last_pattern]    
            result.append(row_data)
        
    insert_query = pattern_match_query()

    with connection.cursor() as cursor:    
        for row_data in result:
            cursor.execute(insert_query, row_data)

    connection.commit()
    connection.close()


with DAG(
    dag_id="candle_pattern",
    default_args=default_args,
    schedule_interval="30 10 * * *", 
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

