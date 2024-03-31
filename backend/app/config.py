from pydantic import Field
from pydantic_settings import BaseSettings
import os

class Config(BaseSettings):
    pass_my: str = Field(os.getenv('DB_PASS'), env="DB_PASS")
    host_my: str = Field(os.getenv('SERVER_IP'), env="SERVER_IP")

    @property
    def db_url(self) -> str:
        user_name = 'root'
        db_name = 'STOCK_DB'
        return f"mysql+mysqlconnector://{user_name}:{self.pass_my}@{self.host_my}/{db_name}"
    
config = Config()