from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

from datetime import datetime
import exchange_calendars as ecals
import pandas as pd

import time
from database import connection
from sentiment_model import get_news_df, classify_news, get_sentiment_score

from utils import get_stock_table, sentiment_pred_query, logical_date

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

    display = 100
    all_news_data = []

    client_id = "기입 필요"
    client_secret = "기입 필요"

    for row in stock_table:
        query = row['stock_name']
        code = row['stock_code']

        news_data = get_news_df(query, code, client_id, client_secret, display)
        all_news_data.extend(news_data)
        time.sleep(0.1)

    all_news_df = pd.DataFrame(all_news_data)

    sentiments = classify_news(all_news_df['description'].tolist())
    all_news_df['sentiment'] = sentiments

    result = []
    for row in stock_table:
        query = row['stock_name']
        code = row['stock_code']

        try:
            score_dict = get_sentiment_score(all_news_df, query)
            data = list(score_dict.values())
            last = [item[0] for item in data]
            prev = [item[1] for item in data]
            
            row_data = [code, last[0], prev[1], prev[2], prev[3],  last[1], last[2], last[3]]
            result.append(row_data)

        except Exception as e:
            print(f"Error: {e}")
            continue
    
    sql_query = sentiment_pred_query()

    with connection.cursor() as cursor:
        for row_data in result:
            try:
                cursor.execute(sql_query, row_data)
            except Exception as e:
                print(f"Error: {e}")
                continue

    connection.commit()
    connection.close()

with DAG(
    dag_id="sentiment_predict",
    default_args=default_args,
    schedule_interval="0 12 * * *", 
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

    predict_task = PythonOperator(
        task_id="predict_task",
        python_callable=predict,
        op_kwargs={
            'date': execution_date,
        }
    )

    valid_check_task >> [predict_task, close]

