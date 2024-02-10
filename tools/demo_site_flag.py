import yfinance as yf
import streamlit as st
import plotly.graph_objs as go
import graph_matching_tools as gmt
import pandas as pd
import numpy as np
from scipy.stats import linregress 
import os
import base64
from io import BytesIO

# Set title and sidebar
st.title('Stock Price Prediction + Pattern Matching')

with st.sidebar:
    st.header('User Input Features')

    # Choose a stock
    company_options = {
        'Samsung': '005930.KS',
        'Naver': '035420.KS',
        'Kakao': '035720.KS',
        'SK Hynix': '000660.KS'
    }
    company = st.selectbox('Choose a stock', list(company_options.keys()))

    # Select period
    period = st.selectbox('Select period', options=[
        '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y'])

    # Select interval
    interval_options = {
        '1d': ['1m', '2m', '5m', '15m', '30m', '60m', '90m'],
        '5d': ['5m', '15m', '30m', '60m', '90m'],
        '1mo': ['30m', '60m', '90m', '1d'],
        '3mo': ['1d', '5d', '1wk', '1mo'],
        '6mo': ['1d', '5d', '1wk', '1mo'],
        '1y': ['1d', '5d', '1wk', '1mo'],
        '2y': ['1d', '5d', '1wk', '1mo'],
        '5y': ['1d', '5d', '1wk', '1mo'],
        '10y': ['1d', '5d', '1wk', '1mo']
    }
    valid_intervals = interval_options[period]
    interval = st.selectbox('Select interval', options=valid_intervals)

# Get stock data
ticker = company_options[company]
data = yf.download(ticker, period=period, interval=interval)


fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='green', increasing_fillcolor='rgba(0,255,0,0.8)',
        decreasing_line_color='red', decreasing_fillcolor='rgba(255,0,0,0.8)'
    )])

    # 차트 기본 설정
fig.update_layout(title=f'{company} Stock Price', yaxis_title='Price', xaxis_title='Date', xaxis_rangeslider_visible=False)

# Download the data as a CSV file
@st.cache_data
def convert_df_to_csv(data):
    return data.to_csv().encode('utf-8')

csv = convert_df_to_csv(data)  # Convert the DataFrame to a CSV

st.sidebar.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=f'{company}_{period}_{interval}_data.csv',
    mime='text/csv',
)
st.plotly_chart(fig, use_container_width=True)



# "Search Patterns" button click action
if st.sidebar.button('Search Patterns') and not data.empty:

    ohlc = gmt.get_ohlc(data)
    back_candles = 20
    flag_points = gmt.find_flag_points(ohlc, back_candles)
    
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

        # linear regression
        if len(xxmin) > 1 and len(xxmax) > 1:  #
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

        # flag point 시각화
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
        

    st.plotly_chart(fig, use_container_width=True)
