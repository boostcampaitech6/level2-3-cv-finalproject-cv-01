from mplfinance.original_flavor import candlestick_ohlc
from scipy.signal import argrelextrema

import matplotlib.dates as mpdates
import matplotlib.pyplot as plt 
import numpy as np
import os
import pandas as pd
from scipy.stats import linregress
import streamlit as st
import plotly.graph_objs as go
from patterns import rectangle

plt.style.use('seaborn-v0_8-darkgrid')
import matplotlib.dates as mdates

def find_rounding_bottom_points(ohlc, back_candles):
    """
    Find all the rounding bottom points

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
                minim = np.append(minim, ohlc.loc[i, "Close"])
                xxmin = np.append(xxmin, i) 
            if ohlc.loc[i,"Pivot"] == 2:
                maxim = np.append(maxim, ohlc.loc[i,"Close"])
                xxmax = np.append(xxmax, i)

        
        if (xxmax.size <3 and xxmin.size <3) or xxmax.size==0 or xxmin.size==0:
            continue

        # Fit a nonlinear line: ax^2 + bx + c        
        z = np.polyfit(xxmin, minim, 2)

        # Check if the first and second derivatives are for a parabolic function
        if 2*xxmin[0]*z[0] + z[1]*xxmin[0] < 0 and 2*z[0] > 0:
             if z[0] >=2.19388889e-04 and z[1]<=-3.52871667e-02:          
                    all_points.append(candle_idx)
                                    

    return all_points


def save_plot(ohlc, all_points, back_candles, save_dir):
    """
    Save all the rounding bottoms graphs

    :params ohlc         -> dataframe that has OHLC data
    :params all_points   -> rounding bottom points
    :params back_candles -> number of periods to lookback
    :return 
    """
    total = len(all_points)
    for j, point in enumerate(all_points):
        candleid = point

        maxim = np.array([])
        minim = np.array([])
        xxmin = np.array([])
        xxmax = np.array([])

        for i in range(point-back_candles, point+1):
            if ohlc.loc[i,"Pivot"] == 1:
                minim = np.append(minim, ohlc.loc[i, "Close"])
                xxmin = np.append(xxmin, i) 
            if ohlc.loc[i,"Pivot"] == 2:
                maxim = np.append(maxim, ohlc.loc[i,"Close"])
                xxmax = np.append(xxmax, i)
                

        z = np.polyfit(xxmin, minim, 2)
        f = np.poly1d(z)
        
        ohlc_subset = ohlc[point-back_candles-10:point+back_candles+10]
        
        xxmin = np.insert(xxmin,0,xxmin[0]-3)    
        xxmin = np.append(xxmin, xxmin[-1]+3)
        minim_new = f(xxmin)
      
        ohlc_subset_copy = ohlc_subset.copy()
        ohlc_subset_copy.loc[:,"Index"] = ohlc_subset_copy.index

        fig, ax = plt.subplots(figsize=(15,7))

        candlestick_ohlc(ax, ohlc_subset_copy.loc[:, ["Index","Open", "High", "Low", "Close"] ].values, width=0.6, colorup='green', colordown='red', alpha=0.8)
        ax.plot(xxmin, minim_new)

        ax.grid(True)
        ax.set_xlabel('Index')
        ax.set_ylabel('Price')


        fn = f"rounding-bottom-{point}.png"
        # file = os.path.join( dir_,'images','analysis',fn)
        os.makedirs(save_dir, exist_ok=True)
        file = os.path.join(save_dir, fn)

        plt.savefig(file, format="png")
        
        print(f"Completed {round((j+1)/total,2)*100}%")

    return

# def get_ohlc(df):

#     df = df.reset_index()
#     df = df[df['Volume'] != 0]
#     df.reset_index(drop=True, inplace=True)
#     ohlc = df.loc[:, ["Date", "Open", "High", "Low", "Close"]]
#     ohlc["Pivot"] = 0

#     return ohlc

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
    # ohlc["Pivot"] = 0
    ohlc["Pivot"] = ohlc.apply(lambda x: pivot_id(ohlc, x.name, 3, 3), axis=1)
    ohlc['PointPos'] = ohlc.apply(lambda row: pivot_point_position(row), axis=1)
    return ohlc



def fig_rounding_bottom_points(company, fig, ohlc, all_points, back_candles):

    fig.update_layout(title=f'{company} Stock Price with rounding_bottom patterns', yaxis_title='Price', xaxis_title='Date', xaxis_rangeslider_visible=False)

    local_max = argrelextrema(ohlc["Close"].values, np.greater)[0]
    local_min = argrelextrema(ohlc["Close"].values, np.less)[0]   

    # start_date = ohlc['Date']    
    # print("start_date", start_date)
    # Set max points to `2` 
    for m in local_max:
        ohlc.loc[m, "Pivot"] = 2
        
    # Set min points to `1`
    for m in local_min:
        ohlc.loc[m, "Pivot"] = 1

    for j, point in enumerate(all_points):
        # candleid = point

        maxim = np.array([])
        minim = np.array([])
        xxmin = np.array([])
        xxmax = np.array([])

        for i in range(point-back_candles, point+1):
            if ohlc.loc[i,"Pivot"] == 1:
                minim = np.append(minim, ohlc.loc[i, "Close"])
                xxmin = np.append(xxmin, ohlc.loc[i, "Date"])
            if ohlc.loc[i,"Pivot"] == 2:
                maxim = np.append(maxim, ohlc.loc[i,"Close"])
                xxmax = np.append(xxmax, ohlc.loc[i, "Date"])

        z = np.polyfit(xxmin, minim, 2)
        f = np.poly1d(z)
        
        ohlc_subset = ohlc[point-back_candles-10:point+back_candles+10]
        xxmin = np.insert(xxmin,0,xxmin[0]-3)    
        xxmin = np.append(xxmin, xxmin[-1]+3)
        minim_new = f(xxmin)
        ohlc_subset_copy = ohlc_subset.copy()
        ohlc_subset_copy.loc[:,"Index"] = ohlc_subset_copy.index
        # print("xxmin", xxmin)
        xxmin_dates = [mdates.num2date(x) for x in xxmin]
        # print("xxmin_dates", xxmin_dates)
        # xxmin_extended = np.linspace(min(xxmin), max(xxmin), 100)
        # minim_new = f(xxmin_extended)

        fig.add_trace(go.Scatter(
            # x=[xxmin[0], xxmin[-1]],
            x=xxmin_dates,
            y=minim_new,
            mode='lines',
            name='Fitted Curve'
        ))

        # 기본 설정을 업데이트합니다.
        # fig.update_layout(
        #     title=f'rounding_bottom for {company}',
        #     yaxis_title='Price',
        #     xaxis_title='Date',
        #     xaxis_rangeslider_visible=False
        # )

    return fig


def plot_rounding_bottom(data, company, base_fig, success_patterns):
    ohlc_rounding_bottom = rectangle.get_ohlc(data)
    back_candles_rounding_bottom = 20
    rounding_bottom_points = find_rounding_bottom_points(ohlc_rounding_bottom, back_candles_rounding_bottom)
    
    if rounding_bottom_points:
        success_patterns.append("rounding_bottom")
        rounding_bottom_fig = go.Figure(base_fig)
        rounding_bottom_fig = fig_rounding_bottom_points(company, rounding_bottom_fig, ohlc_rounding_bottom, rounding_bottom_points, back_candles_rounding_bottom)
        st.plotly_chart(rounding_bottom_fig, use_container_width=True)

    return rounding_bottom_points


if __name__ == "__main__":
    # dir_ = os.path.realpath('').split("research")[0]
    # file = os.path.join( dir_,'data','eurusd-4h.csv') 
    dir_ = os.path.dirname(os.getcwd()) 
    # file = '/data/ephemeral/home/Final_Project/level2-3-cv-finalproject-cv-01/stock_data/naver_data.csv'
    file = '/data/ephemeral/home/Final_Project/pattern_matching/data/Naver_10y_1d_data.csv'
    df = pd.read_csv(file)

    # Remove all non-trading periods
    df=df[df['Volume']!=0]
    df.reset_index(drop=True, inplace=True)


    ohlc = df.loc[:, ["Date", "Open", "High", "Low", "Close"] ]
    ohlc["Date"] = pd.to_datetime(ohlc["Date"])
    # ohlc["Date"] = pd.to_datetime(ohlc["Date"], format="%d.%m.%Y %H:%M:%S.%f")
    ohlc["Date"] = ohlc["Date"].map(mpdates.date2num)

    ohlc["Pivot"] = 0


    # Get the minimas and maximas 
    local_max = argrelextrema(ohlc["Close"].values, np.greater)[0]
    local_min = argrelextrema(ohlc["Close"].values, np.less)[0]   

    # Set max points to `2` 
    for m in local_max:
        ohlc.loc[m, "Pivot"] = 2
        
    # Set min points to `1`
    for m in local_min:
        ohlc.loc[m, "Pivot"] = 1

    
    # Find all the rounding bottom points
    back_candles = 20
    all_points = find_rounding_bottom_points(ohlc, back_candles)

    # print('all_points', all_points)
    # Save all the plots
    # save_dir = '/data/ephemeral/home/Final_Project/Graph_matching/code/images/test'
    save_dir= '/data/ephemeral/home/Final_Project/pattern_matching/images'
    save_plot(ohlc, all_points,back_candles, save_dir)


        

