import datetime
from sqlmodel import SQLModel, Field, create_engine
from .config import config

class PredictionResult(SQLModel,table=True):
    id: int = Field(default=None, primary_key=True)
    result: float
    created_at: str = Field(default_factory=datetime.datetime.now)
    
engine = create_engine(config.db_url)