import yfinance as yf
import streamlit as st
import plotly.graph_objs as go

def plot_candlestick_chart(data, company_name):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='green', increasing_fillcolor='rgba(0,255,0,0.8)',
        decreasing_line_color='red', decreasing_fillcolor='rgba(255,0,0,0.8)'
    )])

    # 차트 레이아웃 설정
    fig.update_layout(
        title=f'{company_name} Stock Price',
        yaxis_title='Price',
        xaxis_title='Date',
        xaxis_rangeslider_visible=False
    )
    return fig


# 주식 데이터를 가져오는 함수
def get_stock_data(ticker, period, interval):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    return hist
