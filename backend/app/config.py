from pydantic import Field
from pydantic_settings import BaseSettings
import os

class Config(BaseSettings):
    pass_my: str = Field(os.getenv('DB_PASS'), env="DB_PASS")
    stock_symbol: str = Field(default="airflow_result/korea_stock_symbols_2024-03-08.csv")
    model_pred: str = Field(default="airflow_result/predict_2024-03-08.csv")

    @property
    def db_url(self) -> str:
        user_name = 'admin'
        host_my = '223.130.147.191'
        db_name = 'airflow_test_db'
        return f"mysql+mysqlconnector://{user_name}:{self.pass_my}@{host_my}/{db_name}"
    
config = Config()