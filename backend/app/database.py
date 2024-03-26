from datetime import datetime
from sqlmodel import SQLModel, Field
from .config import config
import sqlalchemy

class UserInfo(SQLModel,table=True):
    id: int = Field(default=None, primary_key=True) # None: guest user
    created_at: str = Field(default_factory=datetime.now)

class FavoriteStocks(SQLModel,table=True):
    user_id: int = Field(primary_key=True)
    stock_code: str = Field(primary_key=True)

class KRX(SQLModel,table=True):
    stock_code: str = Field(primary_key=True)
    stock_name: str
    market: str

class CNNPredHistory(SQLModel,table=True):
    stock_code: str = Field(primary_key=True)
    date: str = Field(primary_key=True)
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

class TimeSeriesPredHistory(SQLModel,table=True):
    stock_code: str = Field(primary_key=True)
    date: str = Field(primary_key=True)
    close: float
    model: str
    pred_1day: float
    pred_2day: float
    pred_3day: float
    pred_4day: float
    pred_5day: float
    pred_6day: float
    pred_7day: float

class BertPredHistory(SQLModel,table=True):
    stock_code: str = Field(primary_key=True)
    date: str = Field(primary_key=True)
    yesterday_positive: int
    yesterday_neutral: int
    yesterday_negative: int
    today_positive: int
    today_neutral: int
    today_negative: int

class CandlePredHistory(SQLModel,table=True):
    stock_code: str = Field(primary_key=True)
    date: str = Field(primary_key=True)
    candle_name: str

engine = sqlalchemy.create_engine(config.db_url)
SQLModel.metadata.create_all(engine)