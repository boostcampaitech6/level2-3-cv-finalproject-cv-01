
import streamlit as st

def app():
    st.title('About us')
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
