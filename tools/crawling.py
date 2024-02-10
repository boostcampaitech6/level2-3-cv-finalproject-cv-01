import yfinance as yf

ticker_symbol = '035720.KS'

# yfinance Ticker 객체 생성
ticker_data = yf.Ticker(ticker_symbol)

# 지정된 기간 동안의 주가 데이터 가져오기
ticker_df = ticker_data.history(period='1d', start='2022-01-31', end='2024-01-31')

# UTC 시간을 KST로 변경하고, 시간을 제거합니다.
ticker_df.index = ticker_df.index.tz_convert('Asia/Seoul').strftime('%Y-%m-%d')

# Dividends와 Stock Splits 컬럼 제거
ticker_df = ticker_df.drop(columns=['Dividends', 'Stock Splits'])

csv_file_path = 'stock_data/kaka_data.csv'

ticker_df.to_csv(csv_file_path)