import FinanceDataReader as fdr 
import yfinance as yf
import schedule
import time
import pandas as pd
from datetime import datetime
from pykrx import stock

def update_and_save_usa_df():
    # Your existing code to update usa_df
    # S&P500 종목 리스트 가져오기 ...
    # 마지막에 DataFrame을 CSV로 저장
    # S&P500 종목 리스트 가져오기
    usa_df = fdr.StockListing('S&P500')

    # 시가총액 정보를 포함할 새로운 컬럼 추가
    usa_df['Market Cap'] = None

    # yfinance를 통해 각 종목의 시가총액 정보를 가져오고, 시가총액으로 데이터프레임을 정렬
    for symbol in usa_df['Symbol']:
        ticker = yf.Ticker(symbol)
        try:
            market_cap = ticker.info['marketCap']
            usa_df.loc[usa_df['Symbol'] == symbol, 'Market Cap'] = market_cap
        except:
            # 시가총액 정보가 없는 경우 무시
            continue

    # 시가총액 정보가 있는 종목만 필터링하고, 시가총액으로 내림차순 정렬 후 상위 20개 종목 선택
    usa_df = usa_df.dropna(subset=['Market Cap']).sort_values('Market Cap', ascending=False).head(20)

    # 선택된 상위 20개 종목에 대한 추가 정보(종가, 시가 등)를 가져오기
    for symbol in usa_df['Symbol']:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        if not hist.empty:
            usa_df.loc[usa_df['Symbol'] == symbol, 'Close'] = hist['Close'].iloc[-1]
            usa_df.loc[usa_df['Symbol'] == symbol, 'Open'] = hist['Open'].iloc[-1]
            usa_df.loc[usa_df['Symbol'] == symbol, 'Volume'] = hist['Volume'].iloc[-1]
            usa_df.loc[usa_df['Symbol'] == symbol, 'Fluctuation Rate'] = (hist['Close'].iloc[-1] - hist['Open'].iloc[-1]) / hist['Open'].iloc[-1] * 100

    # NaN 값 처리 (옵셔널)
    usa_df.fillna(0, inplace=True)

    usa_df.to_csv('stock_df/usa_stocks.csv', index=False)
    print("USA_df updated")

def get_today_date():
    today = datetime.today().strftime('%Y%m%d')
    return today

def update_and_save_korea_df():
    # 오늘 날짜를 'YYYYMMDD' 포맷으로 가져오는 함수
# 한국 주식 시장의 상위 20개 회사의 정보를 수집하는 함수
    today_date = get_today_date()
    korea_df_info = stock.get_market_cap_by_ticker(today_date)
    top_companies = korea_df_info.head(20)

    # 등락률 정보를 담을 DataFrame 생성
    korea_df = pd.DataFrame()

    # 상위 20개 회사의 등락률 정보 가져오기
    for ticker in top_companies.index:
        company_name = stock.get_market_ticker_name(ticker)  # 티커를 회사명으로 변환
        ohlcv = stock.get_market_ohlcv_by_date(fromdate=today_date, todate=today_date, ticker=ticker)
        if not ohlcv.empty:
            fluctuation_rate = ((ohlcv['종가'] - ohlcv['시가']) / ohlcv['시가'] * 100).iloc[0]
        else:
            fluctuation_rate = None  # 또는 다른 플레이스홀더 값, 예를 들어 0 또는 np.nan
        temp_df = pd.DataFrame({
            '회사명': [company_name],
            '티커' : [ticker],
            '시가총액': [top_companies.loc[ticker, '시가총액']],
            '등락률': [fluctuation_rate],
            '시가': [ohlcv['시가'].iloc[0]],
            '종가': [ohlcv['종가'].iloc[0]],
            '거래량': [ohlcv['거래량'].iloc[0]]
        })
        korea_df = pd.concat([korea_df, temp_df], ignore_index=True)

    korea_df['시가총액'] = korea_df['시가총액']/1e8

    korea_df.to_csv('stock_df/korea_stocks.csv', index=False)
    print("korea_df updated")

# Step 1: Fetch data and calculate fluctuation rates
def fetch_index_data(index_symbol):
    index_data = yf.download(index_symbol, period="1d")
    open_price = index_data['Open'][0]
    close_price = index_data['Close'][0]
    fluctuation_rate = (close_price - open_price) / open_price * 100
    return close_price, open_price, fluctuation_rate

def update_stock_summary():
    indices = {
        'NASDAQ': '^IXIC',
        'S&P500': '^GSPC',
        'KOSPI': '^KS11',
        'KOSDAQ': '^KQ11'
    }
    
    data = {}
    for name, symbol in indices.items():
        close, open_, fluc = fetch_index_data(symbol)
        data[name] = {'Close': close, 'Open': open_, 'Fluctuation Rate': fluc}
    
    df = pd.DataFrame(data).T
    df.to_csv('stock_df/summary_data.csv')
    print("summary_data updated")



# 처음 실행 시 바로 데이터 업데이트 및 저장
update_stock_summary()
update_and_save_usa_df()
update_and_save_korea_df()

# 2시간마다 데이터 업데이트 및 저장을 예약
schedule.every(2).hours.do(update_stock_summary)
schedule.every(2).hours.do(update_and_save_usa_df)
schedule.every(2).hours.do(update_and_save_korea_df)


while True:
    schedule.run_pending()
    time.sleep(1)
