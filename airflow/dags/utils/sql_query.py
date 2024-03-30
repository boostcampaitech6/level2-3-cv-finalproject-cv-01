
def update_stock_query():
    table = 'krx'
    return f"""INSERT INTO {table} (stock_code, stock_name, market, date) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE date=VALUES(date)
    """
    
def get_stock_table(db_connection, date):
    krx_table = "krx"
    with db_connection.cursor() as cursor:
        query = f"SELECT * FROM {krx_table} WHERE date = '{date}'"
        cursor.execute(query)
        stock_table = cursor.fetchall()

    return stock_table

def cnn_pred_query():
    cnn_pred_table = "cnnpredhistory"

    return f"""
            INSERT INTO {cnn_pred_table}
            (stock_code, date, close, 
            pred_1day_result, pred_1day_percent, 
            pred_2day_result, pred_2day_percent, 
            pred_3day_result, pred_3day_percent, 
            pred_4day_result, pred_4day_percent, 
            pred_5day_result, pred_5day_percent, 
            pred_6day_result, pred_6day_percent, 
            pred_7day_result, pred_7day_percent) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            close = VALUES(close),
            pred_1day_result = VALUES(pred_1day_result),
            pred_1day_percent = VALUES(pred_1day_percent),
            pred_2day_result = VALUES(pred_2day_result),
            pred_2day_percent = VALUES(pred_2day_percent),
            pred_3day_result = VALUES(pred_3day_result),
            pred_3day_percent = VALUES(pred_3day_percent),
            pred_4day_result = VALUES(pred_4day_result),
            pred_4day_percent = VALUES(pred_4day_percent),
            pred_5day_result = VALUES(pred_5day_result),
            pred_5day_percent = VALUES(pred_5day_percent),
            pred_6day_result = VALUES(pred_6day_result),
            pred_6day_percent = VALUES(pred_6day_percent),
            pred_7day_result = VALUES(pred_7day_result),
            pred_7day_percent = VALUES(pred_7day_percent)
        """

def ts_pred_query():
    table = "timeseriespredhistory"
    return  f"""
        INSERT INTO {table} (stock_code, date, close, model, pred_1day, pred_2day, pred_3day, pred_4day, pred_5day, pred_6day, pred_7day)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        close = VALUES(close),
        pred_1day = VALUES(pred_1day),
        pred_2day = VALUES(pred_2day),
        pred_3day = VALUES(pred_3day),
        pred_4day = VALUES(pred_4day),
        pred_5day = VALUES(pred_5day),
        pred_6day = VALUES(pred_6day),
        pred_7day = VALUES(pred_7day)
    """

def sentiment_pred_query():
    bert_table = "bertpredhistory"
    return f"""
        INSERT INTO {bert_table} (stock_code, date, yesterday_positive, yesterday_neutral, yesterday_negative, today_positive, today_neutral, today_negative)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        yesterday_positive = VALUES(yesterday_positive),
        yesterday_neutral = VALUES(yesterday_neutral),
        yesterday_negative = VALUES(yesterday_negative),
        today_positive = VALUES(today_positive),
        today_neutral = VALUES(today_neutral),
        today_negative = VALUES(today_negative)
    """

def pattern_match_query():
    table = "candlepredhistory"
    return f"""INSERT INTO {table} (stock_code, date, candle_name) 
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE candle_name = VALUES(candle_name)"""




