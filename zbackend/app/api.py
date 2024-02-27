from fastapi import FastAPI
from pydantic import BaseModel

from model import get_CNN5d_5d,get_CNN5d_20d,get_CNN20d_5d,get_CNN20d_20d, inference
from utils import get_stock_data

class StockInfo(BaseModel):
    name: str
    period: str
    interval :str


app = FastAPI()

cnn5d5d = get_CNN5d_5d()
cnn5d20d = get_CNN5d_20d()
cnn20d5d = get_CNN20d_5d()
cnn20d20d = get_CNN20d_20d()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/stock", tags=["stock"])
async def stock_df(stock_info: StockInfo):
    df = get_stock_data(stock_info.name, stock_info.period, stock_info.interval)
    return df.to_json(orient="records")


@app.post("/pred/cnn", tags=["predict"])
async def pred_cnn(stock_info: StockInfo, s_term: int, t_term : int):

    df = get_stock_data(stock_info.name, stock_info.period, stock_info.interval)
    df = df.iloc[-s_term:]
    model_name = f"cnn{s_term}d{t_term}d"
    model = globals()[model_name]

    pred = inference(model, df, s_term)
    
    return pred

