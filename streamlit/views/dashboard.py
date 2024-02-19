# pages/home.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px



def korea_stock_tree():
    korea_df = pd.read_csv('views/stock_df/korea_stocks.csv')
    # 등락률에 따라 색상을 할당하기 위한 색상 범위 설정
    color_group = [-np.inf, -3, -0.01, 0, 0.01, 3, np.inf]
    korea_df['colors'] = pd.cut(korea_df['ChagesRatio'], bins=color_group, labels=['red', 'indianred', 'gray', 'lightgreen', 'lime', 'green'])

    # 트리맵 생성
    fig = px.treemap(korea_df, path=[px.Constant("all"), 'Name'], values='Marcap', color='colors', height=700,
                    color_discrete_map = {
                            '(?)': '#262931',
                            'red': 'rgba(255, 0, 0, 0.8)',  # 80% 불투명도의 빨간색
                            'indianred': 'rgba(205, 92, 92, 0.9)',
                            'gray': 'rgba(128, 128, 128, 0.9)',
                            'lightgreen': 'rgba(144, 238, 144, 0.9)',
                            'lime': 'rgba(0, 255, 0, 0.9)',
                            'green': 'rgba(0, 128, 0, 0.9)'
                        },
                    hover_data={'ChagesRatio': ':.2f'},
                    custom_data=['ChagesRatio', 'Marcap'])

    # 트리맵의 호버 템플릿과 텍스트 템플릿 업데이트
    fig.update_traces(
        hovertemplate="<br>".join([
            "회사명: %{label}",
            "시가총액(억원): %{customdata[1]:,.0f}",
            "등락률: %{customdata[0]:.2f}%"
        ])
    )
    fig.data[0].texttemplate = "<b>%{label}</b><br>%{customdata[0]:.2f}%"

    return fig


def usa_stock_tree():
    usa_df = pd.read_csv('views/stock_df/usa_stocks.csv')
    # 등락률에 따라 색상을 할당하기 위한 색상 범위 설정
    color_group = [-np.inf, -3, -0.01, 0, 0.01, 3, np.inf]
    usa_df['colors'] = pd.cut(usa_df['Fluctuation Rate'], bins=color_group, labels=['red', 'indianred', 'gray', 'lightgreen', 'lime', 'green'])

    # 트리맵 생성
    fig = px.treemap(usa_df, path=[px.Constant("all"), 'Symbol'], values='Market Cap', color='colors', height=700,
                    color_discrete_map={
                            '(?)': '#262931',
                            'red': 'rgba(255, 0, 0, 0.8)',  # 80% 불투명도의 빨간색
                            'indianred': 'rgba(205, 92, 92, 0.9)',
                            'gray': 'rgba(128, 128, 128, 0.9)',
                            'lightgreen': 'rgba(144, 238, 144, 0.9)',
                            'lime': 'rgba(0, 255, 0, 0.9)',
                            'green': 'rgba(0, 128, 0, 0.9)'
                        },
                    hover_data=['Fluctuation Rate', 'Market Cap'])

    # 트리맵의 호버 템플릿과 텍스트 템플릿 업데이트
    fig.update_traces(
        hovertemplate="<br>".join([
            "회사명: %{label}",
            "시가총액: %{customdata[1]:,.0f}",
            "등락률: %{customdata[0]:.2f}%"
        ])
    )
    fig.data[0].texttemplate = "<b>%{label}</b><br>%{customdata[0]:.2f}%"

    return fig


def app():
    st.title("Stock Market Summary")

    summary_df = pd.read_csv('views/stock_df/summary_data.csv', names=['Index', 'Close', 'Open', 'Fluctuation Rate'])
    # Streamlit 대시보드 레이아웃 설정
    m1, m2, m3, m4= st.columns((1,1,1,1))

    # 지수별로 데이터 필터링 및 표시
    for index, row in summary_df.iterrows():
        index_name = row['Index']
        current_value = row['Close']
        previous_value = row['Open']
        fluctuation_rate = row['Fluctuation Rate']
        
        # 선택한 컬럼에 지수 정보 표시
        if index_name == 'NASDAQ':
            m1.metric(label='NASDAQ', value=f"{float(current_value):.2f}", delta=f"{float(fluctuation_rate):.2f}%", delta_color="inverse")
        elif index_name == 'S&P500':
            m2.metric(label='S&P500', value=f"{float(current_value):.2f}", delta=f"{float(fluctuation_rate):.2f}%", delta_color="inverse")
        elif index_name == 'KOSPI':
            m3.metric(label='KOSPI', value=f"{float(current_value):.2f}", delta=f"{float(fluctuation_rate):.2f}%", delta_color="inverse")
        elif index_name == 'KOSDAQ':
            m4.metric(label='KOSDAQ', value=f"{float(current_value):.2f}", delta=f"{float(fluctuation_rate):.2f}%", delta_color="inverse")   

    korea_stock_map = korea_stock_tree()
    usa_stock_map = usa_stock_tree()
    
    market_choice = st.radio("", ('KOREA', 'USA'), horizontal=True)

    if market_choice == 'KOREA':
        st.subheader("Korea Market Heatmap")
        st.plotly_chart(korea_stock_map, use_container_width=True)
    elif market_choice == 'USA':
        st.subheader("USA Market Heatmap")
        st.plotly_chart(usa_stock_map, use_container_width=True)
