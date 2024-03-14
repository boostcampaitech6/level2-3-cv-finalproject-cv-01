from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine
from .config import config

class UserInfo(SQLModel,table=True):
    id: int = Field(default=None, primary_key=True) # None: guest user
    created_at: str = Field(default_factory=datetime.now)

class FavoriteStocks(SQLModel,table=True):
    user_id: int 
    stock_code: int = Field(primary_key=True)

class SavePredResults(SQLModel,table=True):
    user_id: int 
    stock_code: int = Field(primary_key=True)
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

class KRX(SQLModel,table=True):
    stock_code: str = Field(primary_key=True)
    stock_name: str

class CNNPredHistory(SQLModel,table=True):
    stock_code: int = Field(primary_key=True)
    date: str = Field(primary_key=True)
    close: str
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
    
engine = create_engine(config.db_url)