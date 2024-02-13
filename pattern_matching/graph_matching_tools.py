from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpdates
import matplotlib.pyplot as plt 
import numpy as np
import os
import pandas as pd
from scipy.stats import linregress
import plotly.graph_objs as go
from scipy.stats import linregress
import numpy as np
from progress.bar import Bar

plt.style.use('seaborn-v0_8-darkgrid')

def pivot_id(ohlc, l, n1, n2):
    """
    Get the pivot id 

    :params ohlc is a dataframe
    :params l is the l'th row
    :params n1 is the number of candles to the left
    :params n2 is the number of candles to the right
    :return int  
    """

    # Check if the length conditions met
    if l-n1 < 0 or l+n2 >= len(ohlc):
        return 0
    
    pivot_low  = 1
    pivot_high = 1

    for i in range(l-n1, l+n2+1):
        if(ohlc.loc[l,"Low"] > ohlc.loc[i, "Low"]):
            pivot_low = 0

        if(ohlc.loc[l, "High"] < ohlc.loc[i, "High"]):
            pivot_high = 0

    if pivot_low and pivot_high:
        return 3

    elif pivot_low:
        return 1

    elif pivot_high:
        return 2
    else:
        return 0


def pivot_point_position(row):
    """
    Get the Pivot Point position and assign the Low or High value

    :params row -> row of the ohlc dataframe
    :return float
    """
   
    if row['Pivot']==1:
        return row['Low']-1e-3
    elif row['Pivot']==2:
        return row['High']+1e-3
    else:
        return np.nan


def get_ohlc(df):
    df = df.reset_index()
    df = df[df['Volume'] != 0]
    df.reset_index(drop=True, inplace=True)
    ohlc = df.loc[:, ["Date", "Open", "High", "Low", "Close"]]
    # ohlc.rename(columns={'Datetime': 'Date'}, inplace=True)  # 'Date' 열로 이름 변경
    ohlc["Pivot"] = ohlc.apply(lambda x: pivot_id(ohlc, x.name, 3, 3), axis=1)
    ohlc['PointPos'] = ohlc.apply(lambda row: pivot_point_position(row), axis=1)
    return ohlc


def find_flag_points(ohlc, back_candles):
    """
    Find flag points

    :params ohlc         -> dataframe that has OHLC data
    :params back_candles -> number of periods to lookback
    :return all_points
    """
    all_points = []
    for candle_idx in range(back_candles+10, len(ohlc)):

        maxim = np.array([])
        minim = np.array([])
        xxmin = np.array([])
        xxmax = np.array([])

        for i in range(candle_idx-back_candles, candle_idx+1):
            if ohlc.loc[i,"Pivot"] == 1:
                minim = np.append(minim, ohlc.loc[i, "Low"])
                xxmin = np.append(xxmin, i) 
            if ohlc.loc[i,"Pivot"] == 2:
                maxim = np.append(maxim, ohlc.loc[i,"High"])
                xxmax = np.append(xxmax, i)

        
        if (xxmax.size <3 and xxmin.size <3) or xxmax.size==0 or xxmin.size==0:
        
            continue

        # NaN 값 처리 추가
        slmin, intercmin, rmin, pmin, semin = linregress(xxmin, minim)
        slmax, intercmax, rmax, pmax, semax = linregress(xxmax, maxim)
  
        # Check if the lines are parallel 
        if abs(rmax)>=0.9 and abs(rmin)>=0.9 and (slmin>=1e-3 and slmax>=1e-3 ) or (slmin<=-1e-3 and slmax<=-1e-3):
                        if (slmin/slmax > 0.9 and slmin/slmax < 1.05): # The slopes are almost equal to each other

                            all_points.append(candle_idx)
                            

    return all_points


def plot_flag_points(company, fig, ohlc, flag_points, back_candles):

    fig.update_layout(title=f'{company} Stock Price with flag patterns', yaxis_title='Price', xaxis_title='Date', xaxis_rangeslider_visible=False)

    for j, point in enumerate(flag_points):
        xxmin, yymin = [], []
        xxmax, yymax = [], []

        for i in range(point - back_candles, point + 1):
            if ohlc.loc[i, "Pivot"] == 1:
                yymin.append(ohlc.loc[i, "Low"])
                xxmin.append(ohlc.loc[i, "Date"])
            if ohlc.loc[i, "Pivot"] == 2:
                yymax.append(ohlc.loc[i, "High"])
                xxmax.append(ohlc.loc[i, "Date"])

        if len(xxmin) > 1 and len(xxmax) > 1:
            min_indices = np.array(range(len(xxmin)))
            slmin, intercmin, _, _, _ = linregress(min_indices, yymin)
            max_indices = np.array(range(len(xxmax)))
            slmax, intercmax, _, _, _ = linregress(max_indices, yymax)

            yymin_line = slmin * min_indices + intercmin
            yymax_line = slmax * max_indices + intercmax

            fig.add_trace(go.Scatter(
                x=[xxmin[0], xxmin[-1]],
                y=[yymin_line[0], yymin_line[-1]],
                mode='lines',
                name='Min Line',
                line=dict(color='orange', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=[xxmax[0], xxmax[-1]],
                y=[yymax_line[0], yymax_line[-1]],
                mode='lines',
                name='Max Line',
                line=dict(color='blue', width=2)
            ))

        flag_date = ohlc.loc[point, 'Date']
        flag_high_price = ohlc.loc[point, 'High']
        flag_low_price = ohlc.loc[point, 'Low']
        
        fig.add_trace(go.Scatter(
            x=[flag_date],
            y=[flag_high_price],
            mode='markers',
            name='Flag High Point',
            marker=dict(color='blue', size=10),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=[flag_date],
            y=[flag_low_price],
            mode='markers',
            name='Flag Low Point',
            marker=dict(color='orange', size=10),
            showlegend=False
        ))

    return fig
