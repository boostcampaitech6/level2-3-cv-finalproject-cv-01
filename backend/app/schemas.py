from pydantic import BaseModel
from datetime import datetime

class UserInfoResponse(BaseModel):
    id: int
    created_at: datetime

class FavoriteStocksResponse(BaseModel):
    user_id: int
    stock_code: int

class SavePredResultsResponse(BaseModel):
    user_id: int
    stock_code: int
    date: str
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

class KRXResponse(BaseModel):
    code: str 
    name: str

class CNNPredResponse(BaseModel):
    stock_code: int 
    date: str 
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