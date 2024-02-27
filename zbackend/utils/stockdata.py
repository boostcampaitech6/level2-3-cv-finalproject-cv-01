import yfinance as yf
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

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


def get_stock_data(name, period, interval):
        ticker = company_options[name]
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        hist.reset_index(drop=False, inplace=True)
        return hist
