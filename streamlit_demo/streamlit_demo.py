import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
from models import cnn_model_inference

def app():
    
    st.markdown(
    """
    # 📈 Predicting Stocks with CNN!

주식 시장은 방대한 양의 데이터와 복잡한 비선형적 특성을 가지고 있습니다. 이러한 다이내믹한 데이터를 정확히 분석하고 모델링하기 위해서는 숨겨진 패턴과 시장의 기본 원리를 효과적으로 파악할 수 있는 최적화된 기술이 필요합니다. 여기서 CNN(합성곱 신경망) 모델의 사용은 중요한 역할을 합니다.

CNN은 이미지 인식과 처리 분야에서 뛰어난 성능을 보이는 기술입니다. 우리 서비스는 과거 주식 가격의 변동을 이미지로 변환하고, 이러한 이미지를 분석하여 미래의 주가 움직임을 예측합니다. CNN 모델은 이미지 속에 숨어있는 복잡한 패턴과 추세를 감지하고 학습함으로써, 시계열 데이터만으로는 파악하기 어려운 관계와 특징을 찾아냅니다.

이 방법은 기존의 수치 기반 시계열 분석과는 차별화된 접근 방식을 제공합니다. 시각적 데이터에서 특징을 추출하고 학습하는 CNN의 능력을 활용하여, 주식 시장의 미묘한 변화와 숨겨진 패턴을 보다 정밀하게 포착할 수 있습니다. 이를 통해 보다 정확하고 신뢰할 수 있는 주가 예측을 제공하고자 합니다.

---

# ✨ How to use it?

1. 메뉴바에서 `Prediction`을 눌러주세요. ✋
2. `Choose a stock`에서 미래 주가가 궁금한 종목을 선택해 주세요. 🧑‍💻
3. 조회하고 싶은 기간과 간격을 설정해 주세요. 🗓️
4. 이제 `Prediction` 버튼만 누르면 우리 모델이 열심히 예측할 거에요! 👀
5. 추가적으로 `Candle matching`을 누르면 캔들 매칭을 통한 정보도 확인 가능해요! 😎

---

# 📛 Disclaimer

모든 데이터와 정보는 정보 제공 목적으로만 제공됩니다. 그 어떤 데이터와 정보도 일반적인 자문이나 맞춤형 자문 같은 투자 자문으로 간주되지 않습니다. 모델의 예측 결과는 여러분의 투자 형태와 투자 목적 또는 기대치에 적합하지 않을 수 있습니다. 

---
"""
)
    st.title("Stock Prediction")


    st.caption(f"주식 시장의 미래를 예측합니다. CNN 모델을 활용하여 주가의 움직임을 예측합니다.  ")
    
    


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
    st.caption(f"아래에서 원하는 종목과 기간을 선택하세요.")
    
    company = st.selectbox('원하는 주식 종목을 선택하세요.', company_list, index=default_company_index)
    st.caption(f"현재 선택할 수 있는 종목은 Tesla, Apple, Google, Nvidia, Samsung, Naver, Kakao, SK Hynix, BTC-USD 입니다.")
    # 기간 선택
    
    period_options = ['1mo', '3mo', '6mo', '1y']
    default_period_index = period_options.index('1mo')
    period = st.selectbox('원하는 기간을 선택하세요.', options=period_options, index=default_period_index)
    st.caption(f"1개월 부터 1년까지의 기간을 선택할 수 있습니다.")

    # 간격 선택 (기간에 따른 간격 선택 제한)
    interval_options = {
        '1mo': '1d',
        '3mo': '1d',
        '6mo': '1d',
        '1y': '1d'
    }
    interval = interval_options[period]

    ticker = company_options[company]
    data = yf.download(ticker, period=period, interval=interval)

    # 캔들스틱 차트 그리기
    fig = go.Figure(data=[go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    # increasing_line_color='#00FFAB', increasing_fillcolor='rgba(0,255,171,0.8)',
                    # decreasing_line_color='#FF865E', decreasing_fillcolor='rgba(255,134,94,0.8)'
        )])

    fig.update_layout(title=f'{company} Stock Price', xaxis_title='Date', yaxis_title='Price', xaxis_rangeslider_visible=False)

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


    # CNN 모델 예측 결과
    cnn_model_inference(company, ticker, period, interval)


    st.markdown("""
---
                """)

    st.title("About us")
    st.markdown(
    """

## **네이버 부스트캠프 AI Tech 6기**
## **CV-01조 Team 내돈내산**
"""
)
    html_code = """
    <br/>
<table>
    <tr height="160px">
        <td align="center" width="150px">
            <a href="https://github.com/minyun-e"><img height="110px"  src="https://github.com/Eddie-JUB/Portfolio/assets/71426994/6ac5b0db-2f18-4e80-a571-77c0812c0bdc"></a>
            <br/>
            <a href="https://github.com/minyun-e"><strong>김민윤</strong></a>
            <br />
        </td>
        <td align="center" width="150px">
            <a href="https://github.com/2018007956"><img height="110px"  src="https://github.com/Eddie-JUB/Portfolio/assets/71426994/cabba669-dda2-4ead-9f73-00128c0ae175"/></a>
            <br/>
            <a href="https://github.com/2018007956"><strong>김채아</strong></a>
            <br />
        </td>
        <td align="center" width="150px">
            <a href="https://github.com/Eddie-JUB"><img height="110px"  src="https://github.com/Eddie-JUB/Portfolio/assets/71426994/2829c82d-ecc8-49fd-9cb3-ae642fbe7513"/></a>
            <br/>
            <a href="https://github.com/Eddie-JUB"><strong>배종욱</strong></a>
            <br />
        </td>
        <td align="center" width="150px">
            <a href="https://github.com/FinalCold"><img height="110px" src="https://github.com/Eddie-JUB/Portfolio/assets/71426994/fdeb0582-a6f1-4d70-9d08-dc2f9639d7a5"/></a>
            <br />
            <a href="https://github.com/FinalCold"><strong>박찬종</strong></a>
            <br />
        </td>
        <td align="center" width="150px">
            <a href="https://github.com/MalMyeong"><img height="110px" src="https://github.com/Eddie-JUB/Portfolio/assets/71426994/0583f648-d097-44d9-9f05-58102434f42d"/></a>
            <br />
            <a href="https://github.com/MalMyeong"><strong>조명현</strong></a>
            <br />
        </td>
        <td align="center" width="150px">
              <a href="https://github.com/classaen7"><img height="110px"  src="https://github.com/Eddie-JUB/Portfolio/assets/71426994/2806abc1-5913-4906-b44b-d8b92d7c5aa5"/></a>
              <br />
              <a href="https://github.com/classaen7"><strong>최시현</strong></a>
              <br />
          </td>
    </tr>
</table>  
<br/>
<br/>

"""


    st.markdown(html_code, unsafe_allow_html=True)
    st.markdown(
    """
사용자들에게 새로운 활용 가능성과 즐거움을 제공하는 서비스 개발을 목표로 모인 팀, 내돈내산입니다! 
우리는 일반적인 시계열 데이터 분석을 넘어 금융 데이터를 새로운 시각으로 탐색하고자 합니다. 

기존의 금융 분석 방식에서 벗어나, 이미지로 변환된 주식 데이터를 이용합니다. 
이미지 데이터와 CNN 모델을 활용하면 주식 데이터를 시각적으로 분석하고, 
주가의 움직임을 보다 직관적으로 파악할 수 있습니다. 

투자자들은 우리 서비스를 통해 더 시각적이고 직관적인 정보를 제공받기에 
시장에서 긍정적인 의사결정을 할 수 있습니다.
"""
)

if __name__ == "__main__":
    app()