import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import time
import numpy as np
import torch 
from PIL import Image
from .cnn_inference import get_CNN5d_5d, get_CNN5d_20d, get_CNN20d_5d, get_CNN20d_20d, inference, image_to_np, grad_cam, image_to_tensor, time_calc

def get_stock_data(ticker, period, interval):
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        return hist

def cnn_model_inference(company, ticker, period, interval):

    pred_progress = ["Data Loading", "Rasterizing", "Analyzing", "Predicting"]

    # 데이터 및 모델 미리 호출
    df = get_stock_data(ticker, period, interval)

    model_5_5 = get_CNN5d_5d()
    model_5_20 = get_CNN5d_20d()
    model_20_5 = get_CNN20d_5d()
    model_20_20 = get_CNN20d_20d()

    
    st.header('Stock Predict by CNN Model', divider='grey')
    
    st.markdown('''CNN 기반 주가 예측 모델입니다.  
                왼쪽의 메뉴바에서 period와 interval을 조정하면 위의 주가 그래프가 변경됩니다.  
                모델은 위의 주가 그래프의 마지막 5개의 캔들 혹은 20개의 캔들을 통해 향후 주가를 예측합니다.  
                아래의 입력 기간과 출력 기간을 설정하면 모델이 향후 주가의 상승/하락을 예측합니다.
                ''')
    st.caption('''(예시)  
               :blue[왼쪽의 메뉴바에서 interval을 1m(1분)으로 설정하고 아래의 입력 Interval을 20으로 설정하면, 모델 예측에 20m(20분)의 데이터가 들어갑니다.]  
               * 이때 위의 주식 그래프의 데이터 수가 입력 Interval 수보다 작으면 에러가 발생합니다.  
               * 주가 그래프의 캔들 수는 입력 Interval 수 보다 많아야 합니다!''')
    
    st.text('')
    st.text('')
    # 5 interval
    st.markdown('''##### 입력/출력 기간을 설정한 뒤 Predict 버튼을 누르시오''')
    
    sb_1,sb_2= st.columns(2)

    with sb_1:
        i_p = sb_1.selectbox('입력 데이터 Interval 수', options=[5, 20])
    with sb_2:    
        o_p = sb_2.selectbox('예측 데이터 Interval 수', options=[5, 20])

    input_period, output_period = time_calc(interval,i_p), time_calc(interval,o_p)
    
    cp, bt = st.columns([7,1])
    
    cp.caption(f"최근 :blue[**{input_period}**]동안 의 데이터를 통해 :blue[**{output_period}**] 이후의 주가 상승/하락을 예측합니다")


    if bt.button('Predict'):
        
        if i_p == 5 and o_p == 5:
            model = model_5_5
        elif i_p == 5 and o_p == 20:
            model = model_5_20
        elif i_p == 20 and o_p == 5:
            model = model_20_5
        elif i_p == 20 and o_p == 20:
            model = model_20_20

        model_pred = inference(model,df,i_p)
        if len(df) < i_p:
            st.error('주가 그래프의 캔들 수는 입력 Interval 수 보다 많아야 합니다. Period를 늘리거나 Interval 수를 줄이시오', icon="🚨")
        else:
            input = image_to_tensor(df,i_p)

            my_bar = st.progress(0, text="progress")

            col1, col2, col3 = st.columns([2,1,1])
            for i,p in enumerate(pred_progress):
                my_bar.progress(25*(i+1), text = p)
                time.sleep(0.8)

                if i == 0:
                    s_data = df.iloc[-i_p:]
                    fig = go.Figure(data=[go.Candlestick(
                        x=s_data.index,
                        open=s_data['Open'],
                        high=s_data['High'],
                        low=s_data['Low'],
                        close=s_data['Close'],
                        increasing_line_color='#00FFAB', increasing_fillcolor='rgba(0,255,171,0.8)',
                        decreasing_line_color='#FF865E', decreasing_fillcolor='rgba(255,134,94,0.8)'
                    )])
                    fig.update_layout(
                        title=f'                          \tInput Data Loaded',
                        yaxis_title='Price (KRW)',
                        xaxis_title='Date',
                        xaxis_rangeslider_visible=False
                    )
                    col1.plotly_chart(fig, use_container_width=True)

                elif i == 1: # Rasterizing
                    col2.text(" ")
                    col2.text(" ")
                    col2.markdown("**Rasterized Image**")
                    for i in range(int(i_p*0.4)):
                        col2.text(" ")
                    col2.image(np.flipud(image_to_np(df,i_p)), clamp=True, caption='Rasterized_image')

                elif i == 2: # Analyzing
                    col3.text(" ")
                    col3.text(" ")
                    col3.markdown("**Grad CAM**")
                    for i in range(int(i_p*0.4)):
                        col3.text(" ")
                    col3.image(np.flipud(grad_cam(model,input)), clamp=True, caption='GradCAM_image')
                    
                else: # Predict
                    st.markdown("#### Prediction")
                    p_col1, p_col2 = st.columns(2)
                    p_col2.text(" ")
                    p_col2.text(" ")
                    p_col2.text(" ")
                    p_col2.text(" ")
                    p_col2.text(" ")
                    p_col2.text(" ")
                    p_col2.text(" ")
                    
                    pred_idx = torch.argmax(model_pred).item()
                    percent = round(model_pred[pred_idx].item()*100,2)

                    if pred_idx == 0:
                        img = Image.open('models/cnn/bear.png').resize((256,256))
                        p_col1.image(img)
                        p_col2.markdown(f'''AI 모델의 분석 결과  
                                        **{company}**의 **{output_period}** 이후 주가는  
                                        :red[**{percent}%**] 확률로 :red[**하락**]을 예측합니다''')
                    elif pred_idx == 1:
                        img = Image.open('models/cnn/bull.png').resize((256,256))
                        p_col1.image(img)
                        p_col2.markdown(f'''AI 모델의 분석 결과  
                                        **{company}**의 **{output_period}** 이후 주가는  
                                        :blue[**{percent}%**] 확률로 :blue[**상승**]을 예측합니다''')
                    

            my_bar.empty()

