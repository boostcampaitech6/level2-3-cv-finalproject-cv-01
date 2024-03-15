from pydantic import Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    db_url: str = Field(default="sqlite:///./db.sqlite3", env="DB_URL")
    stock_symbol: str = Field(default="airflow_result/korea_stock_symbols_2024-03-08.csv")
    model_pred: str = Field(default="airflow_result/predict_2024-03-08.csv")
    
config = Config()