import streamlit as st
from streamlit_option_menu import option_menu  # 추가
# 페이지 모듈 임포트
from views import home, dashboard, prediction, candle_matching, about_us
st.set_page_config(layout="wide")
# 옵션 메뉴를 사이드바에 추가
with st.sidebar:
    selected = option_menu("Main Menu", ["Home", "Dashboard", "Prediction", "Candle Matching", "About Us"],
                           icons=["house", "bi-clipboard-check", "bi-graph-up-arrow", "bar-chart-line", "person lines fill"],
                           menu_icon="cast", default_index=0,
                        #    icons: https://icons.getbootstrap.com/
                           styles={
                               "container": {"padding": "5!important", "background-color": "#fafafa"},
                               "icon": {"color": "orange", "font-size": "25px"}, 
                               "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                               "nav-link-selected": {"background-color": "#02ab21"},
                           })

# # 선택된 페이지에 따라 해당 페이지 함수 호출
if selected == "Home":
    home.app()
elif selected == "Dashboard":
    dashboard.app()
elif selected == "Prediction":
    prediction.app()
elif selected == "Candle Matching":
    candle_matching.app()
elif selected == "About Us":
    about_us.app()