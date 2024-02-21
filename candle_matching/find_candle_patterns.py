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
import streamlit as st
import plotly.graph_objs as go
from .candle_rankings import candle_rankings
from .pattern_descriptions import descriptions
import seaborn as sns
sns.set()

plt.rcParams.update({'figure.figsize':(15,7), 'figure.dpi':120})


def cleanPx(stock, freq='1H'):

    if freq == '1wk':
        freq = 'W'

    elif freq == '1mo':
        freq = 'M'

    else:
        freq = 'min'


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

def detect_candle_patterns(period, interval, stock):

    stock.reset_index(inplace=True)

    if interval in  ['1d', '5d', '1wk', '1mo'] :

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


    elif interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m']:

        stock.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
        stock.set_index('Datetime', inplace=True)

        candle_names = talib.get_function_groups()['Pattern Recognition']
        removed = ['CDLCOUNTERATTACK', 'CDLLONGLINE', 'CDLSHORTLINE', 
                'CDLSTALLEDPATTERN', 'CDLKICKINGBYLENGTH']
        candle_names = [name for name in candle_names if name not in removed]

        stock.reset_index(inplace=True)
        stock = stock[['Datetime', 'Open', 'High', 'Low', 'Close']]
        stock.columns = ['Datetime', 'Open', 'High', 'Low', 'Close']

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

    found_pattern_nums = int(len(stock.candlestick_pattern)) - int((stock.candlestick_pattern == "").sum())

    return stock, found_pattern_nums


def visualize_candle_matching(data, period, interval, tickvals, ticktext, show_bull_patterns, show_bear_patterns, show_recent_candles):

    stock = cleanPx(data, interval)
    stock.reset_index(inplace=False)
    
    if show_recent_candles:
        stock = stock.tail(20)
    
    stock_patterns, found_pattern_nums = detect_candle_patterns(period, interval, stock)

    
    if found_pattern_nums > 0:

        if interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m']:

                    fig = go.Figure(data=[go.Candlestick(
                    x=stock_patterns['Datetime'],
                    open=stock_patterns['Open'],
                    high=stock_patterns['High'],
                    low=stock_patterns['Low'],
                    close=stock_patterns['Close'],
                    name='Candlesticks'
                    )])

        else:
            fig = go.Figure(data=[go.Candlestick(
                x=stock_patterns['Date'],
                open=stock_patterns['Open'],
                high=stock_patterns['High'],
                low=stock_patterns['Low'],
                close=stock_patterns['Close'],
                name='Candlesticks'
            )])
        
        
        for i, row in stock_patterns.iterrows():

            if row['candlestick_match_count'] > 0:

                pattern_name = row['candlestick_pattern']
                description = descriptions.get(pattern_name, "No description available.").replace('\n', '<br>')
            
                if interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m']:
                    if ('Bull' in pattern_name and show_bull_patterns) or ('Bear' in pattern_name and show_bear_patterns):                        
                        fig.add_annotation(
                        x=row['Datetime'], 
                        y=row['High'], 
                        text=row['candlestick_pattern'],
                        hovertext=description,
                        showarrow=True,
                        arrowhead=1,
                        ax=0,
                        ay=-40,
                        align='left', 
                        )

                        fig.update_layout(
                        title='Candlestick Pattern Match',
                        yaxis_title='Price (KRW)',
                        xaxis_title='Datetime',
                        xaxis_rangeslider_visible=False,
                        xaxis_type='category'
                        )


                        if period == '1d':
                            fig.update_xaxes(
                                tickmode='array',
                                tickvals=tickvals,
                                ticktext=ticktext,
                                type='category'
                            )

                        else:
                            fig.update_xaxes(
                            tickmode='array',
                            tickvals=tickvals,
                            ticktext=ticktext,
                            type='category'
                        )

                else:
                    if ('Bull' in pattern_name and show_bull_patterns) or ('Bear' in pattern_name and show_bear_patterns):                        
                        fig.add_annotation(
                        x=row['Date'], 
                        y=row['High'], 
                        text=row['candlestick_pattern'],
                        hovertext=description,
                        showarrow=True,
                        arrowhead=1,
                        ax=0,
                        ay=-40,
                        align='left', 
                        )

                        fig.update_layout(
                        title='Candlestick Pattern Match',
                        yaxis_title='Price (KRW)',
                        xaxis_title='Date',
                        xaxis_rangeslider_visible=False,
                        xaxis_type='category'
                        )
                fig.update_xaxes(
                    tickmode='array',
                    tickvals=tickvals,
                    ticktext=ticktext,
                    type='category'
                )



    # 캔들스틱 패턴이 없는 경우
    else:
        fig.update_layout(
                    title='Candlestick Pattern Match')
        fig.add_annotation(
            x=0.5,  # x position (0.5 for the middle of the plot)
            y=0.5,  # y position (0.5 for the middle of the plot)
            xref="paper",  # refers to the whole x axis (paper position)
            yref="paper",  # refers to the whole y axis (paper position)
            text="No candlestick patterns found in the selected period",  # the text to display
            showarrow=False,  # no arrow for this annotation
            font=dict(size=20)  # font size of the text
        )

    return fig, stock_patterns






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