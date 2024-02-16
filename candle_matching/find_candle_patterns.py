import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=Warning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pandas as pd
import numpy as np
import time
import math
import os.path
from tqdm.notebook import tqdm
from datetime import timedelta, datetime
from dateutil import parser
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# %matplotlib inline
from itertools import compress
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.dates import MonthLocator
import talib
import yfinance as yf
from candle_rankings import candle_rankings
import seaborn as sns
sns.set()

plt.rcParams.update({'figure.figsize':(15,7), 'figure.dpi':120})


def cleanPx(stock, freq='1H'):

    stock = stock.reset_index().rename(columns={'Datetime': 'Date'})

    if 'Datetime' in stock.columns:

        stock = stock.iloc[stock.Datetime.drop_duplicates(keep='last').index]
        stock.Datetime = pd.to_datetime(stock.Datetime)
        stock.set_index('Datetime', inplace=True)
        
        stock_ohlc = stock[['Open','High','Low','Close']]
        stock_vol = stock[['Volume']]

        stock_ohlc = stock_ohlc.resample(freq).agg({'Open': 'first', 
                                    'High': 'max', 
                                    'Low': 'min', 
                                    'Close': 'last'})
        stock_vol = stock_vol.resample(freq).sum()

        stock = pd.concat([stock_ohlc, stock_vol], axis=1)
        # stock.index = stock.index.tz_localize('UTC').tz_convert('Asia/Seoul')

        return stock.dropna()

    
    elif 'Date' in stock.columns:

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
        # stock.index = stock.index.tz_localize('UTC').tz_convert('Asia/Seoul')

        return stock.dropna()

    
    elif 'timestamp' in stock.columns and 'volume' in stock.columns and 'close_time' in stock.columns:

        stock = stock.iloc[stock.timestamp.drop_duplicates(keep='last').index]
        stock.timestamp = pd.to_datetime(stock.timestamp)
        stock.set_index('timestamp', inplace=True)

        stock_ohlc = stock[['open','high','low','close']]
        stock_vol = stock[['volume']]

        stock_ohlc = stock_ohlc.resample(freq).agg({'open': 'first', 
                                    'high': 'max', 
                                    'low': 'min', 
                                    'close': 'last'})
        stock_vol = stock_vol.resample(freq).sum()

        stock = pd.concat([stock_ohlc, stock_vol], axis=1)
        # stock.index = stock.index.tz_localize('UTC').tz_convert('Asia/Seoul')

        return stock.dropna()

    else:
        print('case_4', 'No matching columns')

def detect_candle_patterns(stock):

    stock.reset_index(inplace=True)
    stock.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    stock.set_index('Date', inplace=True)

    candle_names = talib.get_function_groups()['Pattern Recognition']
    removed = ['CDLCOUNTERATTACK', 'CDLLONGLINE', 'CDLSHORTLINE', 
            'CDLSTALLEDPATTERN', 'CDLKICKINGBYLENGTH']
    candle_names = [name for name in candle_names if name not in removed]

    stock.reset_index(inplace=True)
    stock = stock[['Date', 'Open', 'High', 'Low', 'Close']]
    stock.columns = ['Date', 'Open', 'High', 'Low', 'Close']

    # extract OHLC 
    op = stock['Open']
    hi = stock['High']
    lo = stock['Low']
    cl = stock['Close']

    # create columns for each pattern
    for candle in candle_names:
        # below is same as;
        # df["CDL3LINESTRIKE"] = talib.CDL3LINESTRIKE(op, hi, lo, cl)
        stock[candle] = getattr(talib, candle)(op, hi, lo, cl)

    stock['candlestick_pattern'] = np.nan
    stock['candlestick_match_count'] = np.nan


    for index, row in stock.iterrows():

        # no pattern found
        if len(row[candle_names]) - sum(row[candle_names] == 0) == 0:
            stock.loc[index,'candlestick_pattern'] = "NO_PATTERN"
            stock.loc[index, 'candlestick_match_count'] = 0
        # single pattern found
        elif len(row[candle_names]) - sum(row[candle_names] == 0) == 1:
            # bull pattern 100 or 200
            if any(row[candle_names].values > 0):
                pattern = list(compress(row[candle_names].keys(), row[candle_names].values != 0))[0] + '_Bull'
                stock.loc[index, 'candlestick_pattern'] = pattern
                stock.loc[index, 'candlestick_match_count'] = 1
            # bear pattern -100 or -200
            else:
                pattern = list(compress(row[candle_names].keys(), row[candle_names].values != 0))[0] + '_Bear'
                stock.loc[index, 'candlestick_pattern'] = pattern
                stock.loc[index, 'candlestick_match_count'] = 1
        # multiple patterns matched -- select best performance
        else:
            # filter out pattern names from bool list of values
            patterns = list(compress(row[candle_names].keys(), row[candle_names].values != 0))
            container = []
            for pattern in patterns:
                if row[pattern] > 0:
                    container.append(pattern + '_Bull')
                else:
                    container.append(pattern + '_Bear')
            rank_list = [candle_rankings[p] for p in container]
            if len(rank_list) == len(container):
                rank_index_best = rank_list.index(min(rank_list))
                stock.loc[index, 'candlestick_pattern'] = container[rank_index_best]
                stock.loc[index, 'candlestick_match_count'] = len(container)

        # clean up candle columns
    try:
        stock.drop(candle_names, axis = 1, inplace = True)
    except:
        pass

    stock.loc[stock.candlestick_pattern == 'NO_PATTERN', 'candlestick_pattern'] = ''
    stock.candlestick_pattern = stock.candlestick_pattern.apply(lambda x: x[3:])

    return stock



if __name__ == '__main__':

    file = '/data/ephemeral/home/Final_Project/level2-3-cv-finalproject-cv-01/pattern_matching/data/Naver_2y_1d_data.csv'
    OUTPUT_FOLDER = '/data/ephemeral/home/Final_Project/level2-3-cv-finalproject-cv-01/candle_matching/output'

    stock = pd.read_csv(file, parse_dates=True)

    stock = cleanPx(stock, '1D')
    # stock = cleanPx(stock, '1H')
    # stock.reset_index(inplace=True)
    stock.reset_index(inplace=False)
    
    result_stock_with_patterns = detect_candle_patterns(stock)
    # print(result_stock_with_patterns.head(10))

    result_stock_with_patterns.to_csv(OUTPUT_FOLDER + 'test.csv', index=False)