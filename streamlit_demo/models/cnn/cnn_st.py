import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import time
import pandas as pd
import numpy as np
import torch 
from PIL import Image
from .cnn_inference import get_CNN5d_5d, get_CNN5d_20d, get_CNN20d_5d, get_CNN20d_20d, inference, image_to_np, grad_cam, image_to_tensor, time_calc
from datetime import datetime

def get_stock_data(ticker, period, interval):
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        return hist

def cnn_model_inference(company, ticker, period, interval):

    pred_progress = ["Data Loading", "Predicting"]

    # 데이터 및 모델 미리 호출
    df = get_stock_data(ticker, period, interval)

    model_5_5 = get_CNN5d_5d()
    model_5_20 = get_CNN5d_20d()
    model_20_5 = get_CNN20d_5d()
    model_20_20 = get_CNN20d_20d()

    
    # st.header('Stock Predict by CNN Model', divider='grey')
    
   
    
    # st.markdown('''이미지 기반 CNN 인공지능 모델로 주가를 예측합니다.
    #             위의 주가 그래프의 마지막 5일 및 20일의 주식 정보를 통해 향후 주가를 예측합니다.  
    #             아래의 "주가 예측하기" 버튼을 누르면 예측 결과를 확인할 수 있습니다.
    #             ''')
    st.markdown(
    """
    ### 2. 주가를 예측해봐요!

    과연 {company} 주가는 어떻게 변할까요?  \n
    아래의 주가예측하기 버튼을 클릭해서 
    알려주가AI와 함께 확인해볼까요?
    """.format(company=company)
    )
    # st.text('')
    # st.text('')
    
    # cp, bt = st.columns([7,1])
    
    # st.caption(f"최근 :blue[**{5}**]일 및 :blue[**{20}**]일 동안의 데이터를 통해 :blue[**{5}**]일 및 :blue[**{20}**]일 이후의 :blue[**{company}**] 주가 상승/하락을 예측합니다")
    # cp.caption(f"최근 :blue[**{5}**]일 및 :blue[**{20}**]일 동안의 데이터를 통해 :blue[**{5}**]일 및 :blue[**{20}**]일 이후의 :blue[**{company}**] 주가 상승/하락을 예측합니다")
    # col1, col2, col3 = st.columns([1,1,1])

    # st.markdown(f'''
    #             과연 {company} 주가는 어떻게 변할까요?  \n
    #             알려주가AI와 함께 확인해볼까요?
    #             ''')
                    


    
    button_style = """
                        <style>
                        div.stButton > button:first-child {
                            height: 3em;     /* Increase button height */
                            width: 100%;     /* Set button width to 100% of the column */
                            font-size: 1.5em; /* Increase font size */
                        }
                        </style>
                    """
    st.markdown(button_style, unsafe_allow_html=True)

    predict_button = st.button(f'{company} 주가 예측하기')


    if predict_button:
    # if st.button('주가 예측하기', key='predict', help='Click to predict stock prices', **{'class': 'big-button'}):
        
        # Case-1: 5d_5d
        i_p, o_p =5, 5
        input_period, output_period = time_calc(interval,5), time_calc(interval,5)
        model = model_5_5
        model_pred_5 = inference(model,df,i_p)
        my_bar = st.progress(0, text="progress")
        col1, col2, col3 = st.columns([2,1,1])

        pred_idx_5 = torch.argmax(model_pred_5).item()
        percent_5 = round(model_pred_5[pred_idx_5].item()*100,2)

        # Case-2: 20d_20d
        i_p, o_p =20, 20
        input_period, output_period = time_calc(interval,5), time_calc(interval,5)
        model = model_20_20
        model_pred_20 = inference(model,df,i_p)

        pred_idx_20 = torch.argmax(model_pred_20).item()
        percent_20 = round(model_pred_20[pred_idx_20].item()*100,2)

        year = datetime.today().year 
        month = datetime.today().month
        day = datetime.today().day
        _today = datetime.now()
        today = f'{year}년 {month}월 {day}일'
        _next_5d = _today + pd.Timedelta(days=5)
        next_5d = _next_5d.strftime('%Y년 %m월 %d일')
        _next_20d = _today + pd.Timedelta(days=20)
        next_20d = _next_20d.strftime('%Y년 %m월 %d일')
        for i,p in enumerate(pred_progress):
            my_bar.progress(25*(i+1), text = p)
            time.sleep(0.8)

            p_col1, p_col2 = st.columns(2)
            if i == 0:

                if company == 'BTC-USD':
                    img = Image.open('models/cnn/btc.jpg')
                    # img = Image.open('models/cnn/btc.jpg').resize((300,300))
                elif company == 'Apple':
                    img = Image.open('models/cnn/apple.jpeg')
                    # img = Image.open('models/cnn/apple.jpeg').resize((256,256))
                elif company == 'Google':
                    img = Image.open('models/cnn/ask.jpg')
                    # img = Image.open('models/cnn/ant.png').resize((256,256))
                elif company == 'Nvidia':
                    img = Image.open('models/cnn/nvidia2.jpg')
                    # img = Image.open('models/cnn/nvidia.jpg').resize((256,256))
                elif company == 'Tesla':
                    img = Image.open('models/cnn/tesla.jpg')
                    # img = Image.open('models/cnn/tesla.jpg').resize((256,256))
                elif company == 'Samsung':
                    img = Image.open('models/cnn/samsung.png')
                    # img = Image.open('models/cnn/samsung.png').resize((256,256))
                elif company == 'DOGE-USD':
                    img = Image.open('models/cnn/doge.png')
                    # img = Image.open('models/cnn/ant.jpg').resize((256,256))
                elif company == 'Kakao':
                    img = Image.open('models/cnn/kakao.jpg')
                    # img = Image.open('models/cnn/kakao.jpg').resize((256,256))
                elif company == 'Naver':
                    img = Image.open('models/cnn/기도짤.jpg')
                    # img = Image.open('models/cnn/ant.jpg').resize((256,256))
                else:
                    img = Image.open('models/cnn/ant.jpg').resize((256,256))

                if pred_idx_5 == 0 and pred_idx_20 ==0:
                    p_col1.image(img, use_column_width=True)
                    p_col2.markdown(f'''
                                    \n  
                                    \n  
                                    **알려주가 AI가 {company} 주가를 분석한 결과**  \n
                                    오늘인 **{today}** 기준으로  \n
                                    **5일** 뒤인 **{next_5d}**에는 \n
                                    **{percent_5}%** 확신으로 :red[**하락**]을  \n
                                    **20일** 뒤인 **{next_20d}**에는 \n
                                    **{percent_20}%** 확신으로 :red[**하락**]을 예측했어요!''')
                
                elif pred_idx_5 == 0 and pred_idx_20 ==1:
                    p_col1.image(img, use_column_width=True)
                    p_col2.markdown(f'''
                                    \n
                                    \n
                                    **알려주가 AI가 {company} 주가를 분석한 결과**  \n
                                    오늘인 **{today}** 기준으로  \n
                                    **5일** 뒤인 **{next_5d}**에는 \n
                                    **{percent_5}%** 확신으로 :red[**하락**]을  \n
                                    **20일** 뒤인 **{next_20d}**에는 \n
                                    **{percent_20}%** 확신으로 :blue[**상승**]을 예측했어요!''')
                    
                    
                elif pred_idx_5 == 1 and pred_idx_20 ==0:
                    p_col1.image(img, use_column_width=True)
                    p_col2.markdown(f'''
                                    \n
                                    \n
                                    **알려주가 AI가 {company} 주가를 분석한 결과**  \n
                                    오늘인 {today} 기준으로  \n
                                    **5일** 뒤인 {next_5d}에는 \n
                                    **{percent_5}%** 확신으로 :blue[**상승**]을  \n
                                    **20일** 뒤인 {next_20d}에는 \n
                                    **{percent_20}%** 확신으로 :red[**하락**]을 예측했어요!''')
                    
                
                else:
                    p_col1.image(img, use_column_width=True)
                    # p_col1.image(img)
                    p_col2.markdown(f'''
                                    \n
                                    \n
                                    **알려주가 AI가 {company} 주가를 분석한 결과**  \n
                                    오늘인 **{today}** 기준으로  \n
                                    **5일** 이후인 **{next_5d}**에는 \n
                                    **{percent_5}%** 확신으로 :blue[**상승**]을  \n
                                    **20일** 이후인 **{next_20d}**에는 \n
                                    **{percent_20}%** 확신으로 :blue[**상승**]을 예측했어요!''')

            elif i == 1:
                pass

            my_bar.empty()
