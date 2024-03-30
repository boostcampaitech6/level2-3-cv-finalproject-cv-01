import FinanceDataReader as fdr
from statsmodels.tsa.ar_model import AutoReg
import datetime as dt
import datetime
from dateutil.relativedelta import relativedelta

def ar_stock_prediction(code, date):
    try:
        today = datetime.datetime.strptime(date, "%Y-%m-%d")
        bef = today - relativedelta(months=6)
        bef_date = bef.strftime("%Y-%m-%d")
        
        stock_data_hist = fdr.DataReader(code,bef_date, date)
        
        stock_data_close = stock_data_hist[["Close"]]
        stock_data_close = stock_data_close.asfreq("D", method="ffill")
        stock_data_close = stock_data_close.ffill()

        train_df = stock_data_close
        
        # 모델 lags
        model = AutoReg(train_df["Close"], 30).fit(cov_type="HC0")

        # 현재 데이터의 마지막 날짜부터 일주일 후까지 예측
        last_date = train_df.index[-1]

        start_date = last_date + dt.timedelta(days=1)
        forecast_end_date = last_date + dt.timedelta(days=7)
        
        forecast = model.predict(
            start=start_date,
            end=forecast_end_date,
            dynamic=True,
        )
        return forecast.tolist()
    
    except Exception as e:
        print(f"Error: {e}")
        return None