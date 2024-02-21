# prediction.py
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from models.cnn import cnn_model_inference
from models.hmm import HMM

def app():
    st.title('Stock Price Prediction')
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
        period = st.selectbox('Select period', options=[
            '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y'])

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
        interval = st.selectbox('Select interval', options=valid_intervals)

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
        title=f'{company} Stock Price',
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


    # Non-DL model matching 시각화
    if st.button("Start Non-DL model matching"):        
        hmm = HMM(data)
        predicted_close_prices = hmm.test_predictions()
        fig = hmm.visualize_hmm(predicted_close_prices)
        st.plotly_chart(fig, use_container_width=True) 
        
    # DL model matching 시각화

    # Image-based CNN model matching 시각화
    cnn_model_inference( company, ticker, period, interval)
        
    