from pydantic import Field
from pydantic_settings import BaseSettings
import os

class Config(BaseSettings):
    pass_my: str = Field(os.getenv('DB_PASS'), env="DB_PASS")
    
    @property
    def db_url(self) -> str:
        user_name = 'root'
        host_my = '175.45.200.149'
        db_name = 'STOCK_DB'
        return f"mysql+mysqlconnector://{user_name}:{self.pass_my}@{host_my}/{db_name}"
    
config = Config()