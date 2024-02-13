from mplfinance.original_flavor import candlestick_ohlc

import glob
import matplotlib.dates as mpdates
import matplotlib.pyplot as plt 
import numpy as np
import os
import pandas as pd
from progress.bar import Bar 
from scipy.stats import linregress
from typing import List, Union
import plotly.graph_objs as go
import matplotlib.dates as mdates
import streamlit as st

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

def find_triangle_points(ohlc: pd.DataFrame, backcandles: int, triangle_type: str = "symmetrical") -> List[int]:
    """
    Find the trianle points based on the pivot points

    :params ohlc -> dataframe that has OHLC data
    :type :pd.DataFrame

    :params backcandles -> number of periods to lookback
    :type :int

    :params triangle_type -> Find a symmetrical, ascending or descending triangle? Options: ['symmetrical', 'ascending', 'descending']
    :type :str 

    :returns triangle points
    """
    all_triangle_points = []

    bar = Bar(f'Finding triangle points ', max=len(ohlc))
    for candleid in range(backcandles+10, len(ohlc)):
        
        maxim = np.array([])
        minim = np.array([])
        xxmin = np.array([])
        xxmax = np.array([])

        for i in range(candleid-backcandles, candleid+1):
            if ohlc.loc[i,"Pivot"] == 1:
                minim = np.append(minim, ohlc.loc[i, "Low"])
                xxmin = np.append(xxmin, i) 
            if ohlc.loc[i,"Pivot"] == 2:
                maxim = np.append(maxim, ohlc.loc[i,"High"])
                xxmax = np.append(xxmax, i)

       
        if (xxmax.size <3 and xxmin.size <3) or xxmax.size==0 or xxmin.size==0:
               continue

        slmin, intercmin, rmin, pmin, semin = linregress(xxmin, minim)
        slmax, intercmax, rmax, pmax, semax = linregress(xxmax, maxim)

        if triangle_type == "symmetrical":
            if abs(rmax)>=0.9 and abs(rmin)>=0.9 and slmin>=0.0001 and slmax<=-0.0001:
                all_triangle_points.append(candleid)

        elif triangle_type == "ascending":
            if abs(rmax)>=0.9 and abs(rmin)>=0.9 and slmin>=0.0001 and (slmax>=-0.00001 and slmax <= 0.00001):
                all_triangle_points.append(candleid)
    
        elif triangle_type == "descending":
            if abs(rmax)>=0.9 and abs(rmin)>=0.9 and slmax<=-0.0001 and (slmin>=-0.00001 and slmin <= 0.00001):
                all_triangle_points.append(candleid)

        bar.next()

    bar.finish()
    return all_triangle_points


def plot_pattern(ohlc: pd.DataFrame, all_triangle_points: List[int], backcandles: int, point: int = 0) -> None:
    """
    Plot a single instance of the triangle pattern

    :params ohlc - Dataframe that has all the Open, High, Low, Close
    :type :pd.DataFrame

    :params all_triangle_points - list that has all index points that have triangle points
    :type :List[int]

    :params backcandles - number of periods to lookback
    :type :int

    :params point - The triangle point to plot. It has to be less than the length of all_triangle_points. Default 0; Plot the first triangle point
    :type :int
    """

    total = len(all_triangle_points) 
    if point > total:
        print(f"Error. The `point` has to be less than {total}")    
        return 

    triangle_point = all_triangle_points[point]
    candleid = triangle_point
    
    maxim = np.array([])
    minim = np.array([])
    xxmin = np.array([])
    xxmax = np.array([])

    for i in range(candleid-backcandles, candleid+1):
        if ohlc.loc[i,"Pivot"] == 1:
            minim = np.append(minim, ohlc.loc[i, "Low"])
            xxmin = np.append(xxmin, int(i)) 
        if ohlc.loc[i,"Pivot"] == 2:
            maxim = np.append(maxim, ohlc.loc[i,"High"])
            xxmax = np.append(xxmax, int(i))
            

    slmin, intercmin, rmin, pmin, semin = linregress(xxmin, minim)
    slmax, intercmax, rmax, pmax, semax = linregress(xxmax, maxim)

    ohlc_subset                     = ohlc[candleid-backcandles-10:candleid+backcandles+10]
    ohlc_subset_copy                = ohlc_subset.copy()
    ohlc_subset_copy.loc[:,"Index"] = ohlc_subset_copy.index

    xxmin = np.append(xxmin, xxmin[-1]+15)
    xxmax = np.append(xxmax, xxmax[-1]+15)


    # Move the y-axis to the right hand side. 
    plt.rcParams['ytick.right'] = plt.rcParams['ytick.labelright'] = True
    plt.rcParams['ytick.left'] = plt.rcParams['ytick.labelleft'] = False

    fig, ax = plt.subplots(figsize=(15,7), facecolor='#000000')

    candlestick_ohlc(ax, ohlc_subset_copy.loc[:, ["Index","Open", "High", "Low", "Close"] ].values,
     width=0.6, colorup='green', colordown='red', alpha=0.8)


    # Draw the triangle lines.
    ax.plot(xxmin, xxmin*slmin + intercmin, linewidth=12, color="purple", alpha=0.85)
    ax.plot(xxmax, xxmax*slmax + intercmax, linewidth=12, color="purple", alpha=0.85)


    # Color the ticks white
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    

    ax.set_facecolor('#000000')
    ax.grid(False)
    ax.set_xlabel('Index')
    # ax.set_ylabel('Price')


    plt.show()

    return None 


def save_plot(save_dir, ohlc: pd.DataFrame, all_triangle_points: List[int], backcandles: int, triangle_type) -> None:
    """
    Save all the triangle patterns graphs

    :params ohlc -> dataframe that has OHLC data
    :type :pd.DataFrame 

    :params all_triangle_points -> list that has all index points that have triangle points
    :type :List[int]
    
    :params backcandles -> number of periods to lookback
    :type :int
    
    :return None  
    """
    total = len(all_triangle_points)

    bar  = Bar("Plotting the pattern", max=total)
    for j, triangle_point in enumerate(all_triangle_points):
        candleid = triangle_point
        
        maxim = np.array([])
        minim = np.array([])
        xxmin = np.array([])
        xxmax = np.array([])

        for i in range(candleid-backcandles, candleid+1):
            if ohlc.loc[i,"Pivot"] == 1:
                minim = np.append(minim, ohlc.loc[i, "Low"])
                xxmin = np.append(xxmin, int(i)) 
            if ohlc.loc[i,"Pivot"] == 2:
                maxim = np.append(maxim, ohlc.loc[i,"High"])
                xxmax = np.append(xxmax, int(i))
                

        slmin, intercmin, rmin, pmin, semin = linregress(xxmin, minim)
        slmax, intercmax, rmax, pmax, semax = linregress(xxmax, maxim)

        ohlc_subset = ohlc[candleid-backcandles-10:candleid+backcandles+10]
        ohlc_subset_copy = ohlc_subset.copy()
        ohlc_subset_copy.loc[:,"Index"] = ohlc_subset_copy.index
    
        xxmin = np.append(xxmin, xxmin[-1]+15)
        xxmax = np.append(xxmax, xxmax[-1]+15)


    
        # Move the y-axis to the right hand side. 
        plt.rcParams['ytick.right'] = plt.rcParams['ytick.labelright'] = True
        plt.rcParams['ytick.left'] = plt.rcParams['ytick.labelleft'] = False

        fig, ax = plt.subplots(figsize=(15,7), facecolor='#000000')

        candlestick_ohlc(ax, ohlc_subset_copy.loc[:, ["Index","Open", "High", "Low", "Close"] ].values, width=0.6, colorup='green', colordown='red', alpha=0.8)

        
        # Draw the triangle lines.
        ax.plot(xxmin, xxmin*slmin + intercmin, linewidth=12, color="purple", alpha=0.85)
        ax.plot(xxmax, xxmax*slmax + intercmax, linewidth=12, color="purple", alpha=0.85)


        # Color the ticks white
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        

        ax.set_facecolor('#000000')
        ax.grid(False)

        fn   = f"triangle-{triangle_type}-{triangle_point}.png"

        # file = os.path.join( dir_,'images','analysis',fn)
        os.makedirs(save_dir, exist_ok=True)
        file = os.path.join(save_dir, fn)
        plt.savefig(file, format="png")

        bar.next()

    bar.finish()

    return None

def get_ohlc(df):

    df = df.reset_index()
    df = df[df['Volume'] != 0]
    df.reset_index(drop=True, inplace=True)
    ohlc = df.loc[:, ["Date", "Open", "High", "Low", "Close"]]
    ohlc["Pivot"] = ohlc.apply(lambda x: pivot_id(ohlc, x.name, 15, 15), axis=1)
    ohlc['ShortPivot'] = ohlc.apply(lambda x: pivot_id(df, x.name,5,5), axis=1)
    # ohlc['PointPos'] = ohlc.apply(lambda row: pivot_point_position(row), axis=1)
    return ohlc

def fig_triangle_points(company, fig, ohlc_triangle, points, back_candles):

    fig.update_layout(title=f'{company} Stock Price with flag patterns', yaxis_title='Price', xaxis_title='Date', xaxis_rangeslider_visible=False)

    for point in points:
        xxmin, yymin = [], []
        xxmax, yymax = [], []

        for i in range(point - back_candles, point + 1):
            if ohlc.loc[i, "Pivot"] == 1:
                yymin.append(ohlc.loc[i, "Low"])
                xxmin.append(ohlc.loc[i, "Date"])
            if ohlc.loc[i, "Pivot"] == 2:
                yymax.append(ohlc.loc[i, "High"])
                xxmax.append(ohlc.loc[i, "Date"])

        ohlc_subset = ohlc[point-back_candles-10:point+back_candles+10]
        xxmin = np.insert(xxmin,0,xxmin[0]-3)    
        xxmin = np.append(xxmin, xxmin[-1]+3)
        minim_new = f(xxmin)
        ohlc_subset_copy = ohlc_subset.copy()
        ohlc_subset_copy.loc[:,"Index"] = ohlc_subset_copy.index
        xxmin_dates = [mdates.num2date(x) for x in xxmin]

        fig.add_trace(go.Scatter(
            # x=[xxmin[0], xxmin[-1]],
            x=xxmin_dates,
            y=minim_new,
            mode='lines',
            name='Fitted Curve'
        ))

    return fig

def plot_triangle_pattern(data, company, base_fig, success_patterns):
    triangle_type = "symmetrical" # "ascending", "descending", "symmetrical"
    ohlc_triangle = get_ohlc(data)
    back_candles_triangle = 20
    triangle_points = find_triangle_points(ohlc_triangle, back_candles_triangle, triangle_type)

    if triangle_points:
        success_patterns.append("triangle")
        triangle_fig = go.Figure(base_fig)
        triangle_fig = fig_triangle_points(company, triangle_fig, ohlc_triangle, triangle_points, back_candles_triangle)
        st.plotly_chart(triangle_fig, use_container_width=True)

    return triangle_points



if __name__ == "__main__":
    dir_ = os.path.dirname(os.getcwd())
    # dir_ = os.path.realpath('').split("research")[0]
    # file = os.path.join( dir_,'data','eurusd-4h.csv') 
    file = '/data/ephemeral/home/Final_Project/pattern_matching/data/Naver_10y_1d_data.csv'
    save_dir = '/data/ephemeral/home/Final_Project/pattern_matching/images'
    df   = pd.read_csv(file)

    # Remove all non-trading periods
    df=df[df['Volume']!=0]
    df.reset_index(drop=True, inplace=True)


    ohlc         = df.loc[:, ["Date", "Open", "High", "Low", "Close"] ]
    # ohlc["Date"] = pd.to_datetime(ohlc["Date"], format="%d.%m.%Y %H:%M:%S.%f")
    ohlc["Date"] = pd.to_datetime(ohlc["Date"])
    ohlc["Date"] = ohlc["Date"].map(mpdates.date2num)


    ohlc["Pivot"] = ohlc.apply(lambda x: pivot_id(ohlc, x.name, 3, 3), axis=1)
    ohlc['PointPos'] = ohlc.apply(lambda row: pivot_point_position(row), axis=1)
 
    
    # Identify the triangle patterns
    backcandles         = 20
    all_triangle_points = find_triangle_points(ohlc, backcandles, triangle_type="descending") # symmetrical, ascending, descending

    # Plot the first instance of the found triangle points
    # plot_pattern(ohlc, all_triangle_points, backcandles)

    # Plot all the triangle points and save them to file
    # print('all_triangle_points', all_triangle_points)
    save_plot(save_dir, ohlc, all_triangle_points, backcandles, triangle_type="descending")


   

  