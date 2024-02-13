from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpdates
import matplotlib.pyplot as plt 
import numpy as np
import os
import pandas as pd
from scipy.stats import linregress
from scipy.stats import linregress
import streamlit as st

import plotly.graph_objs as go
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
        if(ohlc.loc[l,"Close"] > ohlc.loc[i, "Close"]):
            pivot_low = 0

        if(ohlc.loc[l, "Close"] < ohlc.loc[i, "Close"]):
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
    Get the Pivot Point position and assign a Close value

    :params row -> row of the ohlc dataframe
    :return float
    """
   
    if row['Pivot']==1:
        return row['Close']-1e-3
    elif row['Pivot']==2:
        return row['Close']+1e-3
    else:
        return np.nan


def find_wedge_points(ohlc, back_candles):
    """
    Find wedge points

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

        slmin, intercmin, rmin, pmin, semin = linregress(xxmin, minim)
        slmax, intercmax, rmax, pmax, semax = linregress(xxmax, maxim)
        

        # Check if the lines are in the same direction
        if abs(rmax)>=0.9 and abs(rmin)>=0.9 and ((slmin>=1e-3 and slmax>=1e-3 ) or (slmin<=-1e-3 and slmax<=-1e-3)):
                # Check if lines are parallel but converge fast 
                x_ =   (intercmin -intercmax)/(slmax-slmin)
                cors = np.hstack([xxmax, xxmin])  
                if (x_ - max(cors))>0 and (x_ - max(cors))<(max(cors) - min(cors))*3 and slmin/slmax > 0.75 and slmin/slmax < 1.25:  
                     all_points.append(candle_idx)
            

    return all_points


def point_position_plot(ohlc, start_index, end_index):
        """
        Plot the pivot points over a sample period

        :params ohlc        -> dataframe that has OHLC data
        :params start_index -> index where to start taking the sample data
        :params end_index   -> index where to stop taking the sample data
        :return 
        """
        ohlc_subset = ohlc[start_index:end_index]
        ohlc_subset_copy = ohlc_subset.copy()
        ohlc_subset_copy.loc[:,"Index"] = ohlc_subset_copy.index 



        fig, ax = plt.subplots(figsize=(15,7))
        candlestick_ohlc(ax, ohlc_subset_copy.loc[:, ["Index","Open", "High", "Low", "Close"] ].values, width=0.6, colorup='green', colordown='red', alpha=0.8)
        ax.scatter(ohlc_subset_copy["Index"], ohlc_subset_copy["PointPos"])

        ax.grid(True)
        ax.set_xlabel('Index')
        ax.set_ylabel('Price')

      
        fn   = f"wedge-pivot-point-sample.png"
        os.makedirs(save_dir, exist_ok=True)
        file = os.path.join(save_dir, fn)
        # file = os.path.join( dir_,'images','analysis',fn)
        plt.savefig(file, format="png")

        return

def save_plot(ohlc, all_points, back_candles, save_dir):
    """
    Save all the wedge graphs

    :params ohlc         -> dataframe that has OHLC data
    :params all_points   -> wedge points
    :params back_candles -> number of periods to lookback
    :return 
    """

    total = len(all_points)
    for j, point in enumerate(all_points):

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
                

        slmin, intercmin, rmin, pmin, semin = linregress(xxmin, minim)
        slmax, intercmax, rmax, pmax, semax = linregress(xxmax, maxim)

        xxmin = np.append(xxmin, xxmin[-1]) 
        xxmax = np.append(xxmax, xxmax[-1])

        ohlc_subset = ohlc[point-back_candles-5:point+back_candles+5]
        ohlc_subset_copy = ohlc_subset.copy()
        ohlc_subset_copy.loc[:,"Index"] = ohlc_subset_copy.index
    
        xxmin = np.append(xxmin, xxmin[-1]+15)
        xxmax = np.append(xxmax, xxmax[-1]+15)

        fig, ax = plt.subplots(figsize=(15,7))

        
        candlestick_ohlc(ax, ohlc_subset_copy.loc[:, ["Index","Open", "High", "Low", "Close"] ].values, width=0.6, colorup='green', colordown='red', alpha=0.8)
        ax.plot(xxmin, xxmin*slmin + intercmin)
        ax.plot(xxmax, xxmax*slmax + intercmax)

        ax.grid(True)
        ax.set_xlabel('Index')
        ax.set_ylabel('Price')

  
        fn = f"wedge-{point}.png"
        # file = os.path.join( dir_,'images','analysis',fn)
        os.makedirs(save_dir, exist_ok=True)
        file = os.path.join(save_dir, fn)
        plt.savefig(file, format="png")
        print(f"Completed {round((j+1)/total,2)*100}%")

    return

# get data
def get_ohlc(df):

    df = df.reset_index()
    df = df[df['Volume'] != 0]
    df.reset_index(drop=True, inplace=True)
    # ohlc         = df.loc[:, ["Date","Open","High","Low","Close","Adj Close","Volume"] ]
    ohlc = df.loc[:, ["Date", "Open", "High", "Low", "Close"]]
    # ohlc["Date"] = pd.to_datetime(ohlc["Date"])
    # ohlc["Date"] = ohlc["Date"].map(mpdates.date2num)
    ohlc["Pivot"] = 0
    ohlc["Pivot"] = ohlc.apply(lambda x: pivot_id(ohlc, x.name, 3, 3), axis=1)
    ohlc['PointPos'] = ohlc.apply(lambda row: pivot_point_position(row), axis=1)
    return ohlc


def fig_wedge_points(company, fig, ohlc, wedge_points, back_candles):

    fig.update_layout(title=f'{company} Stock Price with Wedge Patterns', yaxis_title='Price', xaxis_title='Date', xaxis_rangeslider_visible=False)

    # print('wedge_points', wedge_points)

    for point in wedge_points:
      
        xxmin, yymin = [], []
        xxmax, yymax = [], []

        for i in range(point - back_candles, point + 1):
            if ohlc.loc[i, "Pivot"] == 1:
                yymin.append(ohlc.loc[i, "Close"])  # Low 대신 Close 사용
                xxmin.append(ohlc.loc[i, "Date"])
            if ohlc.loc[i, "Pivot"] == 2:
                yymax.append(ohlc.loc[i, "Close"])  # High 대신 Close 사용
                xxmax.append(ohlc.loc[i, "Date"])


        if len(xxmin) > 1 and len(xxmax) > 1:
            min_indices = np.array(range(len(xxmin)))
            slmin, intercmin, _, _, _ = linregress(min_indices, yymin)
            max_indices = np.array(range(len(xxmax)))
            slmax, intercmax, _, _, _ = linregress(max_indices, yymax)

            yymin_line = slmin * min_indices + intercmin
            yymax_line = slmax * max_indices + intercmax

            # print(xxmin[0], xxmin[-1])
            fig.add_trace(go.Scatter(
                x=[xxmin[0], xxmin[-1]],
                # x=[xxmin[0], xxmin[-1]+15],
                y=[yymin_line[0], yymin_line[-1]],
                mode='lines',
                name='Support Line',
                line=dict(color='orange', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=[xxmax[0], xxmax[-1]],
                # x=[xxmax[0], xxmax[-1]+ 15],
                y=[yymax_line[0], yymax_line[-1]],
                mode='lines',
                name='Resistance Line',
                line=dict(color='blue', width=2)
            ))

            wedge_date = ohlc.loc[point, 'Date']
            wedge_high_price = ohlc.loc[point, 'High']
            wedge_low_price = ohlc.loc[point, 'Low']
            
            fig.add_trace(go.Scatter(
            x=[wedge_date],
            y=[wedge_high_price],
            mode='markers',
            name='Wedge High Point',
            marker=dict(color='blue', size=10),
            showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=[wedge_date],
                y=[wedge_low_price],
                mode='markers',
                name='Wedge Low Point',
                marker=dict(color='orange', size=10),
                showlegend=False
            ))

    return fig

def plot_wedge_pattern(data, company, base_fig, success_patterns):

    ohlc_wedge = get_ohlc(data)
    back_candles_wedge = 20
    wedge_points = find_wedge_points(ohlc_wedge, back_candles_wedge)
    
    if wedge_points:
        success_patterns.append("wedge")
        wedge_fig = go.Figure(base_fig)
        wedge_fig = fig_wedge_points(company, wedge_fig, ohlc_wedge, wedge_points, back_candles_wedge)
        st.plotly_chart(wedge_fig, use_container_width=True)

    return wedge_points




if __name__ == "__main__":
    # dir_ = os.path.realpath('').split("research")[0]
    # file = os.path.join( dir_,'data','eurusd-4h.csv') 
    dir_ = os.path.dirname(os.getcwd()) 
    # file = '/data/ephemeral/home/Final_Project/level2-3-cv-finalproject-cv-01/stock_data/naver_data.csv'
    file = '/data/ephemeral/home/Final_Project/pattern_matching/data/Naver_10y_1d_data.csv'
    file = '/data/ephemeral/home/Final_Project/pattern_matching/data/Naver_5y_1d_data.csv'
    save_dir = '/data/ephemeral/home/Final_Project/pattern_matching/images'
    
    df = pd.read_csv(file)

    # Remove all non-trading periods
    df=df[df['Volume']!=0]
    df.reset_index(drop=True, inplace=True)

    ohlc         = df.loc[:, ["Date","Open","High","Low","Close","Adj Close","Volume"] ]
    # ohlc         = df.loc[:, ["Date", "Open", "High", "Low", "Close"] ]
    ohlc["Date"] = pd.to_datetime(ohlc["Date"])
    ohlc["Date"] = ohlc["Date"].map(mpdates.date2num)

    ohlc["Pivot"] = 0

    # Get the minimas and maximas 
    ohlc["Pivot"]    = ohlc.apply(lambda x: pivot_id(ohlc, x.name, 3, 3), axis=1)
    ohlc['PointPos'] = ohlc.apply(lambda x: pivot_point_position(x), axis=1) # Used for visualising the pivot points


    # Plot sample point positions
    point_position_plot(ohlc, 50, 200)

    # # Find all wedge pattern points
    back_candles = 20
    all_points   = find_wedge_points(ohlc, back_candles)
    # print("all_points", all_points)
    # Plot the wedge pattern graphs
    # save_dir = os.path.join(save_dir, 'wedge')
    save_plot(ohlc, all_points, back_candles, save_dir)
