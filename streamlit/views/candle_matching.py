# prediction.py
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import sys
import time
import base64
from io import BytesIO
# 상위 폴더로 이동 후 candle_matching 폴더를 path에 추가
sys.path.append('../candle_matching') 
import find_candle_patterns, get_candle_info_wiki
from pattern_descriptions import descriptions

def app():
    
    st.title('Candle Matching')
    with st.sidebar:
        st.header('User Input Features')

        # 회사 선택
        company_options = {
        "Tesla": "TSLA",
        "Apple": "AAPL",
        "Google": "GOOGL",
        "Nvidia": "NVDA",
        'Samsung': '005930.KS',
        'Naver': '035420.KS',
        'Kakao': '035720.KS',
        'SK Hynix': '000660.KS',
        "BTC-USD": "BTC-USD"
        }
        company_list = list(company_options.keys())
        default_company_index = company_list.index('Naver')
        company = st.selectbox('Choose a stock', company_list, index=default_company_index)

        # 기간 선택
        period_options = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y']
        default_period_index = period_options.index('1mo')
        period = st.selectbox('Select period', options=period_options, index=default_period_index)


        # 기간에 따른 간격 선택
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
        default_interval_index = valid_intervals.index('1d')
        interval = st.selectbox('Select interval', options=valid_intervals, index=default_interval_index)
        # interval = st.selectbox('Select interval', options=valid_intervals)

    ticker = company_options[company]

    # 주식 데이터를 가져오는 함수
    def get_stock_data(ticker, period, interval):
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        return hist

    # 선택된 회사의 주식 데이터 가져오기
    data = get_stock_data(ticker, period, interval)

    # 캔들스틱 차트 생성
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='#00FFAB', increasing_fillcolor='rgba(0,255,171,0.8)',
        decreasing_line_color='#FF865E', decreasing_fillcolor='rgba(255,134,94,0.8)'
    )])

    # 차트 레이아웃 설정
    fig.update_layout(
        title=f'{company} Stock Price of {period} period with {interval} interval',
        yaxis_title='Price (KRW)',
        xaxis_title='Date',
        xaxis_rangeslider_visible=False
    )

    # x축 레이블 설정을 위한 로직
    # x축 포맷 설정
    if period == '1d':
        # 시간 포맷으로 설정하고, 첫 번째 레이블에만 날짜 표시
        date_format = '%b %d, %Y'
        hour_format = '%H:%M'
        
        # 날짜와 첫 시간을 포함한 첫 번째 레이블 생성
        first_label =  data.index[0].strftime(date_format) + ' ' + data.index[0].strftime(hour_format)
        ticktext = [first_label] + [dt.strftime(hour_format) if (dt.hour % 1 == 0 and dt.minute == 0) else '' for dt in data.index[1:]]
        tickvals = data.index
        
        fig.update_xaxes(
            tickmode='array',
            tickvals=tickvals,
            ticktext=ticktext,
            type='category'
        )
    else:

        if len(data) > 0:
            step_size = max(len(data.index) // 10, 1)
            
            ticktext = [date.strftime('%b %d') for date in data.index[::step_size]]
            tickvals = data.index[::step_size]
            
            fig.update_xaxes(
                tickmode='array',
                tickvals=tickvals,
                ticktext=ticktext,
                type='category'
            )
        else:
            # 데이터가 없는 경우 기본 설정 유지
            fig.update_xaxes(
                type='category'
            )

    st.plotly_chart(fig, use_container_width=True)

    # 캔들스틱 차트 데이터 다운로드
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name=f'{company}_{period}_{interval}_stockdata.csv',
        mime='text/csv',
    )


    # candle matching 시각화

    with st.spinner('Matching Candle Patterns...'):
        # progress_bar = st.progress(0)
        progress_placeholder = st.empty()
        progress_bar = progress_placeholder.progress(0)
        for i in range(100):
            # Update progress bar
            progress_bar.progress(i + 1)
            time.sleep(0.01)  # Sleep for 50 milliseconds

    show_bull_patterns = st.checkbox('Show Bull Patterns', True)
    show_bear_patterns = st.checkbox('Show Bear Patterns', True)
    show_recent_candles = st.checkbox('Show Recent 20 Candles', True)
    
    fig_candle_patterns, stock_patterns_result = find_candle_patterns.visualize_candle_matching(data, period, interval, tickvals, ticktext, show_bull_patterns, show_bear_patterns, show_recent_candles)

    progress_placeholder.empty()
    with st.spinner('Drawing plot...'):

        for i in range(100):
            # Update progress bar
            time.sleep(0.015)  # Sleep for 50 milliseconds

    st.plotly_chart(fig_candle_patterns, use_container_width=True)


    # 캔들스틱 차트 데이터 다운로드
    csv_candle_result = stock_patterns_result.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download candle matching result as CSV",
        data=csv_candle_result,
        file_name=f'{company}_{period}_{interval}_candle_matching_result.csv',
        mime='text/csv',
    )
    