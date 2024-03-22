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
    code: str = Field(primary_key=True)
    name: str
    market: str
    close: str


engine = sqlalchemy.create_engine(config.db_url)
SQLModel.metadata.create_all(engine)