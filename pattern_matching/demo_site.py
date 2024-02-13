import yfinance as yf
import streamlit as st
import plotly.graph_objs as go
from patterns import flag, rectangle, wedge, triangle_pattern, rounding_bottom
from scipy.stats import linregress 

# Set title and sidebar
st.title('Stock Price Prediction + Pattern Matching')

with st.sidebar:
    st.header('CV-01 내돈내산')

    # 검색 기반으로 사용자가 입력하면 해당 주식을 찾아서 보여주게 수정
    
    # Choose a stock
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
    company = st.selectbox('Choose a stock', list(company_options.keys()))

    # Select period
    period = st.selectbox('Select period', options=[
        '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y'])

    # Select interval
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

# Get stock data
ticker = company_options[company]
data = yf.download(ticker, period=period, interval=interval)
success_patterns = None

fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='green', increasing_fillcolor='rgba(0,255,0,0.8)',
        decreasing_line_color='red', decreasing_fillcolor='rgba(255,0,0,0.8)'
    )])

# 차트 기본 설정
fig.update_layout(title=f'{company} Stock Price', yaxis_title='Price', xaxis_title='Date', xaxis_rangeslider_visible=False)

# Download the data as a CSV file
@st.cache_data
def convert_df_to_csv(data):
    return data.to_csv().encode('utf-8')

csv = convert_df_to_csv(data)  # Convert the DataFrame to a CSV

st.sidebar.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=f'{company}_{period}_{interval}_data.csv',
    mime='text/csv',
)


# "Search Patterns" button click action
if st.sidebar.button('Search Patterns') and not data.empty:

    success_patterns = []

    # 기본 fig 생성
    base_fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='green', increasing_fillcolor='rgba(0,255,0,0.8)',
        decreasing_line_color='red', decreasing_fillcolor='rgba(255,0,0,0.8)'
    )])
    base_fig.update_layout(title=f'{company} Stock Price', yaxis_title='Price', xaxis_title='Date', xaxis_rangeslider_visible=False)


    # 1. flag pattern
    flag_points = flag.plot_flag_pattern(data, company, base_fig, success_patterns)
    # flag_points = plot_flag_pattern(data, company, base_fig)

    # 2. rectangle pattern => 잘 안잡히는 패턴 같음
    rectangle_points = rectangle.plot_rectangle_pattern(data, company, base_fig, success_patterns)
        
    # 3. wedge pattern
    wedge_points = wedge.plot_wedge_pattern(data, company, base_fig, success_patterns)
    
    # 4. triangle pattern => 잘 안나옴
    triangle_points = triangle_pattern.plot_triangle_pattern(data, company, base_fig, success_patterns)
            
    # 5. rounding bottom pattern
    rounding_bottom_points = rounding_bottom.plot_rounding_bottom(data, company, base_fig, success_patterns)

    
    print("flag_points", len(flag_points))
    print("rectangle_points", len(rectangle_points))
    print("wedge_points", len(wedge_points))
    print("triangle_points", len(triangle_points))
    print("rounding_bottom_points", len(rounding_bottom_points))
    print("interval", interval)

# 검출된 패턴 출력
with st.sidebar:
    st.header("Discovered Patterns")

    # 초기 설정
    if success_patterns is None:
        st.info("Please press 'Search Patterns'")
    elif not success_patterns:
        st.warning("No patterns found.")
    else: 
        st.success(f"{success_patterns}")


