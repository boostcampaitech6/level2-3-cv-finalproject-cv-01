# prediction.py
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import sys
from statsmodels.tsa.ar_model import AutoReg
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import torch
from .models.lstm.model import LSTM
from .models.lstm.utils import load_data, predict, predict_dates
from models import HMM
from models import cnn_model_inference

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
        
        if period == '1mo' :
            default_interval_index = valid_intervals.index('1d')
            interval = st.selectbox('Select interval', options=valid_intervals, index=default_interval_index)
        else:
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

    # AR model prediction 시각화
    def generate_stock_prediction(stock_ticker, period, interval):
    # Try to generate the predictions
        try:
            # Pull the data for the first security
            stock_data = yf.Ticker(stock_ticker)

            # Extract the data for last 1yr with 1d interval
            stock_data_hist = stock_data.history(period=period, interval=interval)

            # Clean the data for to keep only the required columns
            stock_data_close = stock_data_hist[["Close"]]

            # Change frequency to day
            stock_data_close = stock_data_close.asfreq("D", method="ffill")

            # Fill missing values
            stock_data_close = stock_data_close.fillna(method="ffill")

            # Define training and testing area
            train_df = stock_data_close.iloc[: int(len(stock_data_close) * 0.9) + 1]  # 90%
            test_df = stock_data_close.iloc[int(len(stock_data_close) * 0.9) :]  # 10%

            # Define training model
            model = AutoReg(train_df["Close"], 100).fit(cov_type="HC0")
            # model = ARIMA(train_df["Close"], order=(0,0,0)).fit(trend='nc')

            # Predict data for test data
            predictions = model.predict(
                start=test_df.index[0], end=test_df.index[-1], dynamic=True
            )

            # Predict 90 days into the future
            forecast = model.predict(
                start=test_df.index[0],
                end=test_df.index[-1] + dt.timedelta(days=30),
                dynamic=True,
            )

            # Return the required data
            return train_df, test_df, forecast, predictions
        # If error occurs
        except:
            # Return None
            return None, None, None, None
    
    # Unpack the data
    train_df, test_df, forecast, predictions = generate_stock_prediction(ticker, period, interval)
    
    # Check if the data is not None
    if train_df is not None and (forecast >= 0).all() and (predictions >= 0).all():
        # Add a title to the stock prediction graph
        layout = go.Layout(title='AR Prediction', xaxis=dict(title='Date'), yaxis=dict(title='Stock Price'))
    
        # Create a plot for the stock prediction
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=train_df.index,
                    y=train_df["Close"],
                    name="Train",
                    mode="lines",
                    line=dict(color="blue"),
                ),
                go.Scatter(
                    x=test_df.index,
                    y=test_df["Close"],
                    name="Test",
                    mode="lines",
                    line=dict(color="orange"),
                ),
                go.Scatter(
                    x=forecast.index,
                    y=forecast,
                    name="Forecast",
                    mode="lines",
                    line=dict(color="red"),
                ),
                go.Scatter(
                    x=test_df.index,
                    y=predictions,
                    name="Test Predictions",
                    mode="lines",
                    line=dict(color="green"),
                ),
            ], layout=layout
        )

        # Customize the stock prediction graph
        fig.update_layout(xaxis_rangeslider_visible=False)

        # Use the native streamlit theme.
        st.plotly_chart(fig, use_container_width=True)
        
    # HMM prediction 시각화
    if st.button("Start HMM prediction"): 
        with st.spinner('Wait for model output...'):    
            hmm = HMM(data)
            predicted_close_prices = hmm.test_predictions()
            fig = hmm.visualize_hmm(predicted_close_prices)
    st.plotly_chart(fig, use_container_width=True) 
        

    # DL model prediction 시각화
    data_close = data[["Close"]]
    data_close.fillna(method='pad')
    
    scaler = MinMaxScaler(feature_range=(-1, 1))
    data_close_scaled = scaler.fit_transform(data_close.values.reshape(-1,1))
        
    look_back = 10 # choose sequence length
    x_train, y_train, x_test, y_test = load_data(data_close_scaled, look_back)

    x_train = torch.from_numpy(x_train).type(torch.Tensor)
    x_test = torch.from_numpy(x_test).type(torch.Tensor)
    y_train = torch.from_numpy(y_train).type(torch.Tensor)
    y_test = torch.from_numpy(y_test).type(torch.Tensor)
    
    model = LSTM()
    model_state_dict = torch.load('../streamlit/views/models/lstm/lstm.pth')
    model.load_state_dict(model_state_dict)
    
    # make predictions
    y_test_pred = model(x_test)

    # invert predictions
    y_test_pred = scaler.inverse_transform(y_test_pred.detach().numpy())
    y_test = scaler.inverse_transform(y_test.detach().numpy())

    # close_data 준비
    close_data = scaler.transform(data_close.values.reshape(-1, 1)).flatten()

    forecast = predict(10, model, close_data, look_back, scaler)
    forecast_dates = predict_dates(10, data_close)

    # 결과 시각화
    real_price_trace = go.Scatter(x=data_close[len(data_close)-len(y_test):].index, y=y_test.flatten(), mode='lines', line=dict(color="orange"), name='Real Stock Price')
    predicted_price_trace = go.Scatter(x=data_close[len(data_close)-len(y_test):].index, y=y_test_pred.flatten(), mode='lines', line=dict(color="green"), name='Predicted Stock Price')
    forecast_price_trace = go.Scatter(x=forecast_dates, y=forecast, mode='lines', line=dict(color="red"), name='Forecasted Stock Price')

    layout = go.Layout(title='LSTM Prediction', xaxis=dict(title='Date'), yaxis=dict(title='Stock Price'))
    fig2 = go.Figure(data=[real_price_trace, predicted_price_trace, forecast_price_trace], layout=layout)

    st.plotly_chart(fig2)

    # Image-based CNN model prediction 시각화
    cnn_model_inference(company, ticker, period, interval)
        
    