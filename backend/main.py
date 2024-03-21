from dotenv import load_dotenv
load_dotenv()  # 환경 변수 로드

from fastapi import FastAPI
from typing import List
from utils.newsdata import fetch_news_data
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 요청을 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/news/", response_model=List[dict])
async def get_news(query: str = "삼성전자"):
    news_data = await fetch_news_data(query)
    return news_data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)