from fastapi import APIRouter, HTTPException, status, Body
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from .schemas import UserInfoResponse, FavoriteStocksResponse, KRXResponse, CNNPredResponse, TimeSeriesPredResponse, BertPredResponse, CandlePredResponse
from .database import UserInfo, FavoriteStocks, KRX, CNNPredHistory, TimeSeriesPredHistory, BertPredHistory, CandlePredHistory, engine
from typing import List
from utils.newsdata import fetch_news_data
import httpx
import os

router = APIRouter()

@router.get("/stockinfo", tags=["stock"])
def get_stock_info() -> list[KRXResponse]:
    with Session(engine) as session:
        statement = select(KRX)
        results = session.exec(statement).all()
        return [
            KRXResponse(stock_code=result.code, stock_name=result.name, market=result.market)
            for result in results
        ]


@router.get("/news", response_model=List[dict])
async def get_news(query: str = "삼성전자"):
    news_data = await fetch_news_data(query)
    return news_data


@router.get("/user/info/{user_id}", response_model=UserInfoResponse)
async def get_user_info(user_id: int):
    with Session(engine) as session:
        result = session.query(UserInfo).filter(UserInfo.id == user_id).first()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return result


@router.post("/user/favorite/{user_id}", tags=["user"])
def save_user_favorite(user_id: int, stock_code: str): # if press favorite button
    with Session(engine) as session:
        # UserInfo 에 저장되어 있는 값인지 확인
        user_info = session.query(UserInfo).filter(UserInfo.id == user_id).first()
        if not user_info:
            # `UserInfo`에 `user_id`가 없으면 404 에러를 반환
            raise HTTPException(status_code=404, detail="User not found")

        # 사용자가 존재하면 favorite 저장
        result = FavoriteStocks(user_id=user_id, stock_code=stock_code)
        try:
            session.add(result)
            session.commit()
            session.refresh(result)
        except IntegrityError:
            session.rollback()
            print('Existed')
    return FavoriteStocksResponse(user_id=result.user_id, stock_code=result.stock_code)

@router.get("/user/favorite/{user_id}", tags=["user"])
def get_user_favorite(user_id: int) -> list[FavoriteStocksResponse]:
    with Session(engine) as session:
        # UserInfo에 관련 레코드가 있는지 먼저 확인
        user_exists = session.query(UserInfo).filter(UserInfo.id == user_id).first()
        if not user_exists:
            raise HTTPException(
                detail="User not found", 
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        # user_id로 FavoriteStocks에서 관련 레코드를 모두 찾음
        results = session.query(FavoriteStocks).filter(FavoriteStocks.user_id == user_id).all()
        if not results:
            raise HTTPException(
                detail=f"There's no {user_id}'s favorite stocks", status_code=status.HTTP_404_NOT_FOUND
            )
        return [
            FavoriteStocksResponse(user_id=result.user_id, stock_code=result.stock_code)
            for result in results
        ]


@router.get("/pred/cnn", tags=["predict"])
def get_cnn_pred() -> list[CNNPredResponse]:
    with Session(engine) as session:
        statement = select(CNNPredHistory)
        results = session.exec(statement).all()
        return [
            CNNPredResponse(stock_code=result.stock_code, date=result.date, close=result.close,
                            pred_1day_result=result.pred_1day_result, pred_1day_percent=result.pred_1day_percent,
                            pred_2day_result=result.pred_2day_result, pred_2day_percent=result.pred_2day_percent,
                            pred_3day_result=result.pred_3day_result, pred_3day_percent=result.pred_3day_percent,
                            pred_4day_result=result.pred_4day_result, pred_4day_percent=result.pred_4day_percent,
                            pred_5day_result=result.pred_5day_result, pred_5day_percent=result.pred_5day_percent,
                            pred_6day_result=result.pred_6day_result, pred_6day_percent=result.pred_6day_percent,
                            pred_7day_result=result.pred_7day_result, pred_7day_percent=result.pred_7day_percent)
            for result in results
        ]
    
@router.get("/pred/timeseries", tags=["predict"])
def get_timeseries_pred(model: str) -> list[TimeSeriesPredResponse]:
    with Session(engine) as session:
        results = session.query(TimeSeriesPredHistory).filter(TimeSeriesPredHistory.model == model).all()
        return [
            TimeSeriesPredResponse(stock_code=result.stock_code, date=result.date, close=result.close,
                                   pred_1day=result.pred_1day, pred_2day=result.pred_2day, pred_3day=result.pred_3day, pred_4day=result.pred_4day,
                                   pred_5day=result.pred_5day, pred_6day=result.pred_6day, pred_7day=result.pred_7day)
            for result in results
        ]
    
@router.get("/pred/bert", tags=["predict"])
def get_bert_pred() -> list[BertPredResponse]:
    with Session(engine) as session:
        statement = select(BertPredHistory)
        results = session.exec(statement).all()
        return [
            BertPredResponse(stock_code=result.stock_code, date=result.date,
                            yesterday_positive=result.yesterday_positive, yesterday_neutral=result.yesterday_neutral, yesterday_negative=result.yesterday_negative,
                            today_positive=result.today_positive, today_neutral=result.today_neutral, today_negative=result.today_negative)
            for result in results
        ]
    
@router.get("/pred/candle", tags=["predict"])
def get_candle_pred() -> list[CandlePredResponse]:
    with Session(engine) as session:
        statement = select(CandlePredHistory)
        results = session.exec(statement).all()
        return [
            CandlePredResponse(stock_code=result.stock_code, date=result.date, candle_name=result.candle_name)
            for result in results
        ]
        
        
@router.post("/auth/kakao", tags=["login"])
async def kakao_login(code: str = Body(..., embed=True)):
    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"
    
    payload = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("REST_API_KEY"),  # 카카오 REST API 키
        "redirect_uri": f'http://{os.getenv("SERVER_IP")}:3001/login-kakao',  # 카카오 개발자 설정에 등록한 리다이렉트 URI
        "code": code,  # 카카오 로그인 인증 과정에서 받은 인증 코드
    }
    async with httpx.AsyncClient() as client:
        token_response = await client.post(KAKAO_TOKEN_URL, data=payload)
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Could not retrieve access token from Kakao")

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = await client.get(KAKAO_USER_INFO_URL, headers=headers)
        if user_info_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Could not retrieve user info from Kakao")

        user_info = user_info_response.json()
        kakao_id = user_info["id"]
        nickname = user_info["properties"]["nickname"]
        profile_image = user_info["properties"]["profile_image"]

        with Session(engine) as session:
            existing_user = session.query(UserInfo).filter_by(id=str(kakao_id)).first()
            if existing_user is None:
                user_data = UserInfo(id=str(kakao_id), nickname=nickname)
                session.add(user_data)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    raise HTTPException(status_code=400, detail="User already exists")
        print(user_info)
        return_info = {'kakao_id': kakao_id, 'nickname': nickname, 'profile_image': profile_image}

        return return_info

