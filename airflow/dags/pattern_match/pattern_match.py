import FinanceDataReader as fdr
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import talib
import pandas as pd
import numpy as np

candle_patterns_db_path = './dags/pattern_match/candle_patterns_db.csv'  
candle_patterns_db = pd.read_csv(candle_patterns_db_path)

def get_stock_data(code, date):
    today = datetime.strptime(date, "%Y-%m-%d")
    bef = today - relativedelta(months=1)
    bef_str = bef.strftime("%Y-%m-%d")
    return fdr.DataReader(code, bef_str, date)
    

def cleanPx(stock, freq='1d'):
    stock = stock.reset_index().rename(columns={'Datetime': 'Date'})

    if 'Date' in stock.columns:
        stock = stock.iloc[stock.Date.drop_duplicates(keep='last').index]
        stock.Date = pd.to_datetime(stock.Date)
        stock.set_index('Date', inplace=True)

        stock_ohlc = stock[['Open','High','Low','Close']]
        stock_vol = stock[['Volume']]

        stock_ohlc = stock_ohlc.resample(freq).agg({'Open': 'first', 
                                                    'High': 'max', 
                                                    'Low': 'min', 
                                                    'Close': 'last'})
        stock_vol = stock_vol.resample(freq).sum()

        stock = pd.concat([stock_ohlc, stock_vol], axis=1)
        return stock.dropna()
    else:
        print('No matching columns')
        return None
   
def detect_candle_patterns(stock):
    stock.reset_index(inplace=True)
    stock.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    stock.set_index('Date', inplace=True)

    candle_names = talib.get_function_groups()['Pattern Recognition']
    removed = ['CDLCOUNTERATTACK', 'CDLLONGLINE', 'CDLSHORTLINE', 'CDLSTALLEDPATTERN', 'CDLKICKINGBYLENGTH']
    candle_names = [name for name in candle_names if name not in removed]

    stock.reset_index(inplace=True)
    op, hi, lo, cl = stock['Open'].values, stock['High'].values, stock['Low'].values, stock['Close'].values

    for candle in candle_names:
        stock[candle] = getattr(talib, candle)(op, hi, lo, cl)

    stock['candlestick_pattern'] = np.nan
    stock['candlestick_match_count'] = np.nan


    for index, row in stock.iterrows():
        patterns = {candle: row[candle] for candle in candle_names if row[candle] != 0}
        if patterns:

            # 패턴 이름을 code 형식에 맞게 수정
            patterns_codes = []
            for candle, value in patterns.items():
                suffix = 'Bull' if value > 0 else 'Bear'
                pattern_code = f"{candle}_{suffix}"
                patterns_codes.append(pattern_code)
            stock.loc[index, 'candlestick_pattern'] = ', '.join(patterns_codes)
            stock.loc[index, 'candlestick_match_count'] = len(patterns)
        else:
            stock.loc[index, 'candlestick_pattern'] = None  # NO_PATTERN 대신 None 사용
            stock.loc[index, 'candlestick_match_count'] = 0

    stock.drop(candle_names, axis=1, inplace=True)
    stock.loc[stock.candlestick_pattern == 'NO_PATTERN', 'candlestick_pattern'] = ''

    stock = pd.merge(stock, candle_patterns_db, left_on="candlestick_pattern", right_on="code", how="left")

    return stock