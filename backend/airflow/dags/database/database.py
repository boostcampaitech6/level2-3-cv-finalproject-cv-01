# import datetime
# from sqlmodel import SQLModel, Field, create_engine

# class ValidStock(SQLModel,table=True):
#     id: str = Field(default=None, primary_key=True)
#     name: str
#     code: str
    
    
# class PredictResult(SQLModel, table=True):
#     id: str = Field(default=None, primary_key=True)
#     name: str
#     code: str
#     predictList: list


# engine = create_engine(config.db_url)