from fastapi import APIRouter, HTTPException, status, Body
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from .schemas import UserInfoResponse, FavoriteStocksResponse, StockCode, KRXResponse, CNNPredResponse, TimeSeriesPredResponse, BertPredResponse, CandlePredResponse
from .database import UserInfo, FavoriteStocks, KRX, CNNPredHistory, TimeSeriesPredHistory, BertPredHistory, CandlePredHistory, engine
from typing import List
from utils.newsdata import fetch_news_data
from utils.score import TimeSeriesScore, CNNScore, BERTScore, CANDLEScore
import httpx
import os
import FinanceDataReader as fdr

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

@router.get("/api/stock/{symbol}")
async def get_stock_data(symbol: str):
    df = fdr.DataReader(symbol, '2024-01-01')
    if df.empty:
        return {"error": "No data found for the symbol"}
    
    with Session(engine) as session:
        stock_info = session.query(KRX).filter(KRX.stock_code == symbol).first()
        if stock_info is None:
            raise HTTPException(status_code=404, detail="Stock not found")
        
        latest_data = df.iloc[-1]
        data = {
            "symbol": symbol,
            "stock_name": stock_info.stock_name,
            "close": latest_data['Close'],
            "volume": latest_data['Volume'],
            "change": latest_data['Change'],
        }
        return data

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
def update_user_favorite(user_id: int, stock: StockCode = Body(...)):
    with Session(engine) as session:
        user_exists = session.query(UserInfo).filter(UserInfo.id == user_id).first()
        if not user_exists:
            raise HTTPException(
                detail="User not found", 
                status_code=status.HTTP_404_NOT_FOUND
            )
            
        if stock.like:
            # 좋아요 추가
            try:
                result = FavoriteStocks(user_id=user_id, stock_code=stock.stock_code)
                session.add(result)
                session.commit()
                return {"user_id": user_id, "stock_code": stock.stock_code, "like": stock.like}
            except IntegrityError:
                session.rollback()
                raise HTTPException(status_code=409, detail="Already exists")
        else:
            # 좋아요 삭제
            try:
                result = session.query(FavoriteStocks).filter(FavoriteStocks.user_id == user_id, FavoriteStocks.stock_code == stock.stock_code).one()
                session.delete(result)
                session.commit()
                return {"message": "Like removed"}
            except NoResultFound:
                session.rollback()
                raise HTTPException(status_code=404, detail="Like not found")

@router.get("/user/favorite/{user_id}", response_model=List[FavoriteStocksResponse], tags=["user"])
def get_user_favorite(user_id: int) -> List[FavoriteStocksResponse]:
    # 데이터베이스 세션을 가져오는 의존성
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
            # 사용자의 좋아요한 주식이 없는 경우, 빈 리스트 반환
            return []

        return [FavoriteStocksResponse(user_id=result.user_id, stock_code=result.stock_code) for result in results]


@router.get("/pred/cnn", tags=["predict"])
def get_cnn_pred(stock_code: str) -> list[CNNPredResponse]:
    with Session(engine) as session:
        result = session.query(CNNPredHistory)\
                    .filter(CNNPredHistory.stock_code == stock_code)\
                    .order_by(CNNPredHistory.date.desc())\
                    .first()
        score = CNNScore(result.pred_1day_result, result.pred_1day_percent)
        return [
            CNNPredResponse(stock_code=result.stock_code, date=result.date, close=result.close,
                            pred_1day_result=result.pred_1day_result, pred_1day_percent=result.pred_1day_percent,
                            pred_2day_result=result.pred_2day_result, pred_2day_percent=result.pred_2day_percent,
                            pred_3day_result=result.pred_3day_result, pred_3day_percent=result.pred_3day_percent,
                            pred_4day_result=result.pred_4day_result, pred_4day_percent=result.pred_4day_percent,
                            pred_5day_result=result.pred_5day_result, pred_5day_percent=result.pred_5day_percent,
                            pred_6day_result=result.pred_6day_result, pred_6day_percent=result.pred_6day_percent,
                            pred_7day_result=result.pred_7day_result, pred_7day_percent=result.pred_7day_percent,
                            score=score)
        ]
    
@router.get("/pred/timeseries", tags=["predict"])
def get_timeseries_pred(model: str, stock_code: str) -> list[TimeSeriesPredResponse]:

    with Session(engine) as session:
        result = session.query(TimeSeriesPredHistory)\
                    .filter(TimeSeriesPredHistory.stock_code == stock_code, 
                            TimeSeriesPredHistory.model == model)\
                    .order_by(TimeSeriesPredHistory.date.desc())\
                    .first()

        
        score = TimeSeriesScore(result.close, result.pred_1day)

        return [
        TimeSeriesPredResponse(
            stock_code=result.stock_code,
            date=result.date,
            close=result.close,
            pred_1day=result.pred_1day,
            pred_2day=result.pred_2day,
            pred_3day=result.pred_3day,
            pred_4day=result.pred_4day,
            pred_5day=result.pred_5day,
            pred_6day=result.pred_6day,
            pred_7day=result.pred_7day,
            score=score
        )
    ]
    
@router.get("/pred/bert", tags=["predict"])
def get_bert_pred(stock_code: str) -> list[BertPredResponse]:
    with Session(engine) as session:
        result = session.query(BertPredHistory)\
                    .filter(BertPredHistory.stock_code == stock_code)\
                    .order_by(BertPredHistory.date.desc())\
                    .first()
        score = BERTScore(yesterday_positive=result.yesterday_positive, yesterday_neutral=result.yesterday_neutral, yesterday_negative=result.yesterday_negative,
                            today_positive=result.today_positive, today_neutral=result.today_neutral, today_negative=result.today_negative)

        return [
            BertPredResponse(stock_code=result.stock_code, date=result.date,
                            yesterday_positive=result.yesterday_positive, yesterday_neutral=result.yesterday_neutral, yesterday_negative=result.yesterday_negative,
                            today_positive=result.today_positive, today_neutral=result.today_neutral, today_negative=result.today_negative,
                            score=score)
        ]
    
@router.get("/pred/candle", tags=["predict"])
def get_candle_pred(stock_code: str) -> list[CandlePredResponse]:
    with Session(engine) as session:
        result = session.query(CandlePredHistory)\
                    .filter(CandlePredHistory.stock_code == stock_code)\
                    .order_by(CandlePredHistory.date.desc())\
                    .first()
        
        score = CANDLEScore(result.candle_name)
        return [
            CandlePredResponse(stock_code=result.stock_code, date=result.date, candle_name=result.candle_name, score=score)
        ]
        
@router.post("/auth/kakao", tags=["login"])
async def kakao_login(code: str = Body(..., embed=True)):
    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"
    
    payload = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("REST_API_KEY"),  # 카카오 REST API 키
        "redirect_uri": f'http://{os.getenv("SERVER_IP")}:{os.getenv("PORT")}/login-kakao',  # 카카오 개발자 설정에 등록한 리다이렉트 URI
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
  
        return_info = {'kakao_id': kakao_id, 'nickname': nickname, 'profile_image': profile_image}

        return return_info