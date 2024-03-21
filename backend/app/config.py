from pydantic import Field
from pydantic_settings import BaseSettings

user_name = 'admin'
pass_my = 
host_my = '223.130.147.191'
db_name = 'airflow_test_db'

class Config(BaseSettings):
    db_url: str = Field(default=f"mysql+mysqlconnector://{user_name}:{pass_my}@{host_my}/{db_name}")#, env="DB_URL")
    stock_symbol: str = Field(default="airflow_result/korea_stock_symbols_2024-03-08.csv")
    model_pred: str = Field(default="airflow_result/predict_2024-03-08.csv")
    
config = Config()