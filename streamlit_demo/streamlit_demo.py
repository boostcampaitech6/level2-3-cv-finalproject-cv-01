import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
from models import cnn_model_inference
import streamlit.components.v1 as components
from PIL import Image
import streamlit_analytics


ga_tracking_code = """
                        <!-- Google tag (gtag.js) -->
                        <script async src="https://www.googletagmanager.com/gtag/js?id=G-8QXBPGZNVR"></script>
                        <script>
                        window.dataLayer = window.dataLayer || [];
                        function gtag(){dataLayer.push(arguments);}
                        gtag('js', new Date());

                        gtag('config', 'G-8QXBPGZNVR');
                        </script>
                        """


components.html(ga_tracking_code, height=0)

st.markdown(
                """
                    <!-- Global site tag (gtag.js) - Google Analytics -->
                    <script async src="https://www.googletagmanager.com/gtag/js?id=G-8QXBPGZNVR"></script>
                    <script>
                        window.dataLayer = window.dataLayer || [];
                        function gtag(){dataLayer.push(arguments);}
                        gtag('js', new Date());
                        gtag('config', 'G-**********');
                    </script>
                """, unsafe_allow_html=True)


def app():

    

    # st.set_page_config(layout="wide")
    # 첫 화면
    img = Image.open('첫화면테스트.png')
    st.image(img)

    
    # st.title("알려주가AI 사용 방법")

    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    img_2 = Image.open('demo_1.png')
    st.image(img_2)


    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')

    img_3 = Image.open('demo_2.png')
    st.image(img_3)

    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')

    st.markdown(
                """
                <style>
                .markdown-text-container {
                    text-align: center;
                }
                </style>

                <div class="markdown-text-container">
                <h3> 준비되셨나요? </h3>
                <h3>이제 🤖알려주가AI와 함께</h3>
                <h3>주식 투자의 달인이 되어볼까요?!</h3>
                </div>
                """,
                    unsafe_allow_html=True
                )




    st.text('')
    st.text('')
    st.text('')


    # st.caption(f"주식 시장의 미래를 예측합니다. CNN 모델을 활용하여 주가의 움직임을 예측합니다.  ")


    # 회사 선택
    company_options = {
        "Tesla": "TSLA",
        "Apple": "AAPL",
        "Google": "GOOGL",
        "Nvidia": "NVDA",
        "AMD": "AMD",
        'Samsung': '005930.KS',
        'Naver': '035420.KS',
        'Kakao': '035720.KS',
        # 'SK Hynix': '000660.KS',
        "BTC-USD": "BTC-USD",
        "DOGE-USD": "BTC-USD",
    }
    company_list = list(company_options.keys())
    default_company_index = company_list.index('Nvidia')
    # st.caption(f"아래에서 원하는 종목과 기간을 선택하세요.")
    st.markdown('''
                ### 1. 원하는 주식 종목을 선택하세요.
                ''')
    company = st.selectbox('', company_list, index=default_company_index)
    st.caption(f"현재 선택할 수 있는 종목은 Tesla, Apple, Google, Nvidia, Samsung, Naver, Kakao, BTC-USD, DOGE-USD 입니다.")
    # 기간 선택
    
    period_options = ['1mo', '3mo', '6mo', '1y']
    default_period_index = period_options.index('1mo')

    period = '1mo'
    # period = st.selectbox('원하는 기간을 선택하세요.', options=period_options, index=default_period_index)
    # st.caption(f"1개월 부터 1년까지의 기간을 선택할 수 있습니다.")

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

    fig.update_layout(title=f'📈 최근 1개월 간의 {company} 주가 데이터에요!', xaxis_title='Date', yaxis_title='Price', xaxis_rangeslider_visible=False)

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

    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')


    st.markdown(
    """
     ### 🤖알려주가AI 주가 예측 서비스가 도움이 되셨나요? \n
     아래의 설문을 통해 의견을 남겨주세요! \n
     설문을 완료해주신 분들 중 \n
     추첨을 통해 스타벅스 기프티콘을 드립니다!
     🤖알려주가AI를 더 나은 서비스로 발전시키는데 큰 힘이 됩니다! \n
    """
    )
    # 설문

    # 기본형
    html_content  = """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <div formsappId="65dee1274bfcc0164b71b039"></div>
            </div>
            <script src="https://forms.app/static/embed.js" type="text/javascript" async defer onload="new formsapp('65dee1274bfcc0164b71b039', 'standard', {'width':'90vw','height':'600px','opacity':0.15000000000000002});">
            </script>
                    """

    components.html(html_content, height=600)


    components.html("""
                    
                        <style>
                            .container {
                                background-color: #0f1116; /* Change the background color to black */
                                /* Add other styles such as padding or border if needed */
                            }
                        </style>

                        <div class="container" style="display: flex; justify-content: center; align-items: center; gap: 20px;">

                        # <div style="display: flex; justify-content: center; align-items : center; gap: 20px;">
                            <!-- KakaoTalk Channel Add Button -->
                            <div id="kakao-talk-channel-add-button" data-channel-public-id="_kWpaG" data-size="large" data-support-multiple-densities="true"></div>

                            <!-- KakaoTalk Channel Chat Button -->
                            <div id="kakao-talk-channel-chat-button" data-channel-public-id="_kWpaG" data-title="question" data-size="small" data-color="yellow" data-shape="pc" data-support-multiple-densities="true"></div>

                            <!-- Twitter Share Button -->
                            <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-text="알려주가AI: 인공지능 기반 주가 예측 웹-앱 서비스! 🎈" data-url="https://ai-stock-prediction.streamlit.app/" data-show-count="false">Tweet</a>
                        </div>

                        <script>
                            (function(d, s, id) {
                                var js, fjs = d.getElementsByTagName(s)[0];
                                if (d.getElementById(id)) return;
                                js = d.createElement(s); js.id = id;
                                js.src = 'https://t1.kakaocdn.net/kakao_js_sdk/2.6.0/kakao.channel.min.js';
                                js.integrity = 'sha384-ty4605mXDCz/lA+RRt4bHCRa1c9uIaIi0JrsmmWVxaNJZzu58jMhJK8wAMqDxrYv';
                                js.crossOrigin = 'anonymous';
                                fjs.parentNode.insertBefore(js, fjs);
                            })(document, 'script', 'kakao-js-sdk');
                        </script>
                        <script>
                            window.kakaoAsyncInit = function() {
                                
                                Kakao.Channel.createAddChannelButton({
                                    container: '#kakao-talk-channel-add-button',
                                    channelPublicId: '_kWpaG'
                                });
                                Kakao.Channel.createChatButton({
                                    container: '#kakao-talk-channel-chat-button',
                                    channelPublicId: '_kWpaG'
                                });
                            };
                        </script>
                        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        """, height=120)





    st.markdown("""
                # 📛 Disclaimer
                """)


    img_4 = Image.open('투신자판.png')
    st.image(img_4)

    st.markdown("""
    모든 데이터와 정보는 정보 제공 목적으로만 제공됩니다. 그 어떤 데이터와 정보도 일반적인 자문이나 맞춤형 자문 같은 투자 자문으로 간주되지 않습니다. 모델의 예측 결과는 여러분의 투자 형태와 투자 목적 또는 기대치에 적합하지 않을 수 있습니다. 
                """)

    # About us


    st.title("About us")
    st.markdown(
    """

## **네이버 부스트캠프 AI Tech 6기**
## **CV-01조 Team 내돈내산**
"""
)
    html_code = """
                <table style="border-collapse: collapse; border: none;">
                    <tr height="160px">
                        <td align="center" width="150px" style="border: none;">
                            <a href="https://github.com/minyun-e"><img height="110px" src="https://github.com/Eddie-JUB/Portfolio/assets/71426994/6ac5b0db-2f18-4e80-a571-77c0812c0bdc"></a>
                            <br/>
                            <a href="https://github.com/minyun-e"><strong>김민윤</strong></a>
                        </td>
                        <td align="center" width="150px" style="border: none;">
                            <a href="https://github.com/2018007956"><img height="110px" src="https://github.com/Eddie-JUB/Portfolio/assets/71426994/cabba669-dda2-4ead-9f73-00128c0ae175"></a>
                            <br/>
                            <a href="https://github.com/2018007956"><strong>김채아</strong></a>
                        </td>
                        <td align="center" width="150px" style="border: none;">
                            <a href="https://github.com/Eddie-JUB"><img height="110px" src="https://github.com/Eddie-JUB/Portfolio/assets/71426994/2829c82d-ecc8-49fd-9cb3-ae642fbe7513"></a>
                            <br/>
                            <a href="https://github.com/Eddie-JUB"><strong>배종욱</strong></a>
                        </td>
                    </tr>
                    <tr height="160px">
                        <td align="center" width="150px" style="border: none;">
                            <a href="https://github.com/FinalCold"><img height="110px" src="https://github.com/Eddie-JUB/Portfolio/assets/71426994/fdeb0582-a6f1-4d70-9d08-dc2f9639d7a5"></a>
                            <br/>
                            <a href="https://github.com/FinalCold"><strong>박찬종</strong></a>
                        </td>
                        <td align="center" width="150px" style="border: none;">
                            <a href="https://github.com/MalMyeong"><img height="110px" src="https://github.com/Eddie-JUB/Portfolio/assets/71426994/0583f648-d097-44d9-9f05-58102434f42d"></a>
                            <br/>
                            <a href="https://github.com/MalMyeong"><strong>조명현</strong></a>
                        </td>
                        <td align="center" width="150px" style="border: none;">
                            <a href="https://github.com/classaen7"><img height="110px" src="https://github.com/Eddie-JUB/Portfolio/assets/71426994/2806abc1-5913-4906-b44b-d8b92d7c5aa5"></a>
                            <br/>
                            <a href="https://github.com/classaen7"><strong>최시현</strong></a>
                        </td>
                    </tr>
                </table>

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
    with streamlit_analytics.track(save_to_json='tracked.json'):
        app()
    # app()