import yfinance as yf
import streamlit as st
import plotly.graph_objs as go
from datetime import datetime, timedelta
import sys
sys.path.append('../candle_matching') # 상위 폴더로 이동 후 candle_matching 폴더를 path에 추가
import find_candle_patterns
# import pattern_descriptions
from pattern_descriptions import descriptions




# 애플리케이션 메인 타이틀 및 사이드바 설정
st.title('Stock Price Prediction')
with st.sidebar:
    st.header('User Input Features')

    # 회사 선택
    company_options = {
        'Samsung': '005930.KS',
        'Naver': '035420.KS',
        'Kakao': '035720.KS',
        'SK Hynix': '000660.KS'
    }
    company = st.selectbox('Choose a stock', list(company_options.keys()))

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
    # '1d' 이외의 기간에 대해서는 'Aug 8' 형식으로 날짜 표시
    # 데이터 포인트에 따라 동적으로 tickvals와 ticktext 조정
    if len(data) > 0:
        # 데이터 포인트 간격 계산
        step_size = max(len(data.index) // 10, 1)
        
        # 날짜 포맷을 'Aug 8' 형식으로 조정
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

# 차트 레이아웃 및 Streamlit에 차트 표시 부분은 동일하게 유지

# Streamlit에 차트 표시
st.plotly_chart(fig, use_container_width=True)




# pattern matching 시각화

with st.sidebar:
    show_patterns = st.checkbox('Show Candlestick Patterns', True)

if data.columns[0] == 'Date':
    interval = '1D'

elif data.columns[0] == 'Datetime':
    interval = '1H'

stock = find_candle_patterns.cleanPx(data, interval)
stock.reset_index(inplace=False)
stock_patterns = find_candle_patterns.detect_candle_patterns(stock)

OUTPUT_FOLDER = '/data/ephemeral/home/Final_Project/level2-3-cv-finalproject-cv-01/candle_matching/output/'
# stock_patterns.to_csv(OUTPUT_FOLDER + 'test.csv', index=False)


fig = go.Figure(data=[go.Candlestick(
    x=stock_patterns['Date'],
    open=stock_patterns['Open'],
    high=stock_patterns['High'],
    low=stock_patterns['Low'],
    close=stock_patterns['Close'],
    name='Candlesticks'
)])


if show_patterns:
    for i, row in stock_patterns.iterrows():

        if row['candlestick_match_count'] > 0:

            pattern_name = row['candlestick_pattern']
            description = descriptions.get(pattern_name, "No description available.").replace('\n', '<br>')
        
            fig.add_annotation(
                x=row['Date'], 
                y=row['High'], 
                text=row['candlestick_pattern'],
                hovertext=description,
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40,
                align='left', 
            )


fig.update_layout(
    title='Candlestick Pattern Match',
    yaxis_title='Price (KRW)',
    xaxis_title='Date',
    xaxis_rangeslider_visible=False,
)


st.plotly_chart(fig, use_container_width=True)