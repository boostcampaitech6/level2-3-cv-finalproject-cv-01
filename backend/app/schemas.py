from pydantic import BaseModel
from datetime import datetime

class UserInfoResponse(BaseModel):
    id: int
    created_at: datetime
    nickname: str

class FavoriteStocksResponse(BaseModel):
    user_id: int
    stock_code: int

class KRXResponse(BaseModel):
    stock_code: str 
    stock_name: str
    market: str

class CNNPredResponse(BaseModel):
    stock_code: str 
    date: datetime 
    close: float	    
    pred_1day_result: int
    pred_1day_percent: float
    pred_2day_result: int
    pred_2day_percent: float
    pred_3day_result: int
    pred_3day_percent: float
    pred_4day_result: int
    pred_4day_percent: float
    pred_5day_result: int
    pred_5day_percent: float
    pred_6day_result: int
    pred_6day_percent: float
    pred_7day_result: int
    pred_7day_percent: float
    score: float

class TimeSeriesPredResponse(BaseModel):
    stock_code: str
    date: datetime
    close: float
    pred_1day: float
    pred_2day: float
    pred_3day: float
    pred_4day: float
    pred_5day: float
    pred_6day: float
    pred_7day: float
    score: float

class BertPredResponse(BaseModel):
    stock_code: str
    date: datetime
    yesterday_positive: int
    yesterday_neutral: int
    yesterday_negative: int
    today_positive: int
    today_neutral: int
    today_negative: int
    score: float

class CandlePredResponse(BaseModel):
    stock_code: str
    date: datetime
    candle_name: str
    score: float