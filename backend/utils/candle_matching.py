import yfinance as yf
import talib
import pandas as pd
import numpy as np
from itertools import compress
import os

# Set period and interval as fixed values
period = '1mo'
interval = '1d'


current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
candle_patterns_db_path = os.path.join(current_dir_path, 'candle_patterns_db.csv')
candle_patterns_db = pd.read_csv(candle_patterns_db_path)

def get_stock_data(ticker, period=period, interval=interval):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    return hist

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

def main(ticker):
    stock = get_stock_data(ticker)
    stock = cleanPx(stock)
    stock = detect_candle_patterns(stock)

    # 'candlestick_pattern' 컬럼에서 NaN이 아닌 마지막 값을 가진 행의 인덱스를 찾음
    last_valid_index = stock['candlestick_pattern'].last_valid_index()
    if last_valid_index is not None:
        last_pattern = stock.loc[last_valid_index, 'candlestick_pattern']
        if last_pattern and last_pattern != 'NO_PATTERN':
            # 가장 최근 유효한 패턴에 대한 정보를 검색
            pattern_info = candle_patterns_db[candle_patterns_db['code'].isin([last_pattern])]
            if not pattern_info.empty:
                # 패턴 상세 정보를 딕셔너리 형태로 반환
                pattern_details = pattern_info[['name', 'kor_name', 'up', 'down', 'common_rank', 'efficiency_rank', 'discription']].iloc[0].to_dict()
                return {"message": f"가장 최근 매칭된 패턴: {last_pattern}", "details": pattern_details}
            else:
                return {"message": "패턴 상세 정보를 찾을 수 없습니다."}
        else:
            return {"message": "최근에 매칭된 유효한 패턴이 없습니다."}
    else:
        return {"message": "모든 행이 NaN입니다."}


if __name__ == "__main__":
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "005930.KS"
    main(ticker)
