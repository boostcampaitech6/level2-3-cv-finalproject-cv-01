from fastapi import APIRouter, HTTPException, status, Body, Path, Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from .schemas import UserInfoResponse, FavoriteStocksResponse, SavePredResultsResponse, KRXResponse, CNNPredResponse
from .database import UserInfo, FavoriteStocks, SavePredResults, KRX, CNNPredHistory, engine
from .config import config
from datetime import datetime
import os
import httpx

router = APIRouter()

@router.post("/user", tags=["user"])
def save_user_info(user_id: int): 
    '''
    kakao 인증키가 있는 경우 UserInfo.id에 저장, 비로그인일 경우 id 부여X
    '''
    user = UserInfo(id=user_id)  
    with Session(engine) as session:
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
        except IntegrityError:
            session.rollback()
            print('Existing member')
    return UserInfoResponse(id=user.id, created_at=user.created_at)

@router.get("/user", tags=["user"])
def get_Alluser_info() -> list[UserInfoResponse]:
    with Session(engine) as session:
        statement = select(UserInfo)
        results = session.exec(statement).all()
        return [
            UserInfoResponse(id=result.id, created_at=result.created_at)
            for result in results
        ]

@router.get("/user/{id}", tags=["user"])
def get_user_info(id: int) -> UserInfoResponse:
    with Session(engine) as session:
        result = session.get(UserInfo, id)
        if not result:
            raise HTTPException(
                detail="Not found", status_code=status.HTTP_404_NOT_FOUND
            )
        return UserInfoResponse(
            id=result.id, created_at=result.created_at
        )


@router.post("/user/favorite/{user_id}", tags=["user"])
def save_user_favorite(user_id: int, stock_code: int): # if press favorite button
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


@router.post("/user/saved/{user_id}", tags=["user"])
def save_user_saved(user_id: int, stock_code: str): # if press saved button
    with Session(engine) as session:
        # user_id가 UserInfo에 저장되어 있는 값인지 확인
        user_info = session.query(UserInfo).filter(UserInfo.id == user_id).first()
        if not user_info:
            # `UserInfo`에 `user_id`가 없으면 404 에러를 반환
            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)

        # stock_code가 CNNPredResponse 저장되어 있는 값인지 확인
        pred_info = session.query(CNNPredHistory).filter(CNNPredHistory.stock_code == stock_code).first()
        if not pred_info:
            # `UserInfo`에 `user_id`가 없으면 404 에러를 반환
            raise HTTPException(detail="Prediction result not found", status_code=status.HTTP_404_NOT_FOUND)
        
        date = session.query(CNNPredHistory.date).order_by(CNNPredHistory.date.desc()).first()
        # CNNPredHistory table 조회
        search = session.query(CNNPredHistory).filter(
            CNNPredHistory.stock_code == stock_code,
            CNNPredHistory.date == date.date
            ).first()
        # 사용자가 존재하면 AI 분석 결과 저장
        result = SavePredResults(user_id=user_id, stock_code=stock_code, 
                    date=date.date,
                    pred_1day_result=search.pred_1day_result,pred_1day_percent=search.pred_1day_percent,
                    pred_2day_result=search.pred_2day_result,pred_2day_percent=search.pred_2day_percent,
                    pred_3day_result=search.pred_3day_result,pred_3day_percent=search.pred_3day_percent,
                    pred_4day_result=search.pred_4day_result,pred_4day_percent=search.pred_4day_percent,
                    pred_5day_result=search.pred_5day_result,pred_5day_percent=search.pred_5day_percent,
                    pred_6day_result=search.pred_6day_result,pred_6day_percent=search.pred_6day_percent,
                    pred_7day_result=search.pred_7day_result,pred_7day_percent=search.pred_7day_percent)
        try:
            session.add(result)
            session.commit()
            session.refresh(result)
        except IntegrityError:
            session.rollback()
            print('Existed')
    return SavePredResultsResponse(user_id=result.user_id, stock_code=result.stock_code, date=result.date,
                            pred_1day_result=result.pred_1day_result,pred_1day_percent=result.pred_1day_percent,
                            pred_2day_result=result.pred_2day_result,pred_2day_percent=result.pred_2day_percent,
                            pred_3day_result=result.pred_3day_result,pred_3day_percent=result.pred_3day_percent,
                            pred_4day_result=result.pred_4day_result,pred_4day_percent=result.pred_4day_percent,
                            pred_5day_result=result.pred_5day_result,pred_5day_percent=result.pred_5day_percent,
                            pred_6day_result=result.pred_6day_result,pred_6day_percent=result.pred_6day_percent,
                            pred_7day_result=result.pred_7day_result,pred_7day_percent=result.pred_7day_percent)

@router.get("/user/saved/{user_id}", tags=["user"])
def get_user_saved(user_id: int) -> list[SavePredResultsResponse]:
    with Session(engine) as session:
        # UserInfo에 관련 레코드가 있는지 먼저 확인
        user_exists = session.query(UserInfo).filter(UserInfo.id == user_id).first()
        if not user_exists:
            raise HTTPException(
                detail="User not found", 
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        # user_id로 SavePredResults에서 관련 레코드를 모두 찾음
        results = session.query(SavePredResults).filter(SavePredResults.user_id == user_id).all()
        if not results:
            raise HTTPException(
                detail=f"There's no {user_id}'s saved info", status_code=status.HTTP_404_NOT_FOUND
            )
        return [
            SavePredResultsResponse(user_id=result.user_id, stock_code=result.stock_code, date=result.date,
                pred_1day_result=result.pred_1day_result,pred_1day_percent=result.pred_1day_percent,
                pred_2day_result=result.pred_2day_result,pred_2day_percent=result.pred_2day_percent,
                pred_3day_result=result.pred_3day_result,pred_3day_percent=result.pred_3day_percent,
                pred_4day_result=result.pred_4day_result,pred_4day_percent=result.pred_4day_percent,
                pred_5day_result=result.pred_5day_result,pred_5day_percent=result.pred_5day_percent,
                pred_6day_result=result.pred_6day_result,pred_6day_percent=result.pred_6day_percent,
                pred_7day_result=result.pred_7day_result,pred_7day_percent=result.pred_7day_percent)
                for result in results
        ]
        

@router.post("/stockinfo", tags=["stock"])
def save_stock_info(): 
    file = open(config.stock_symbol,'r')
    file.readline() # drop first row
    for line in file.readlines():
        value, label = line.strip().split(',')
        value = value.split(':')[1]
        stocks = KRX(stock_code=value, stock_name=label)
        with Session(engine) as session:
            session.add(stocks)
            session.commit()
            session.refresh(stocks)
    return KRXResponse(code=stocks.stock_code, name=stocks.stock_name)

@router.get("/stockinfo", tags=["stock"])
def get_stock_info() -> list[KRXResponse]:
    with Session(engine) as session:
        statement = select(KRX)
        results = session.exec(statement).all()
        return [
            KRXResponse(code=result.stock_code, name=result.stock_name)
            for result in results
        ]


@router.post("/pred/cnn", tags=["predict"])
def save_cnn_pred()->CNNPredResponse: 
    file = open(config.model_pred,'r')
    file.readline() # drop first row
    for line in file.readlines():
        Date,Name,Code,Close,Day_1,Day_2,Day_3,Day_4,Day_5,Day_6,Day_7 = line.strip().split(',')[1:]

        result = CNNPredHistory(
            stock_code=Code,#KRX.stock_code, 
            date=Date,#KRX.date,
            close=Close,
            pred_1day_result=Day_1.split('/')[0],
            pred_1day_percent=Day_1.split('/')[1],
            pred_2day_result=Day_2.split('/')[0],
            pred_2day_percent=Day_2.split('/')[1],
            pred_3day_result=Day_3.split('/')[0],
            pred_3day_percent=Day_3.split('/')[1],
            pred_4day_result=Day_4.split('/')[0],
            pred_4day_percent=Day_4.split('/')[1],
            pred_5day_result=Day_5.split('/')[0],
            pred_5day_percent=Day_5.split('/')[1],
            pred_6day_result=Day_6.split('/')[0],
            pred_6day_percent=Day_6.split('/')[1],
            pred_7day_result=Day_7.split('/')[0],
            pred_7day_percent=Day_7.split('/')[1]
        )
        with Session(engine) as session:
            try:
                session.add(result)
                session.commit()
                session.refresh(result)
            except IntegrityError:
                session.rollback()
                print('UNIQUE constraint failed. Check for duplicates in the PK attribute.')

    return CNNPredResponse(
        stock_code=result.stock_code,
        date=result.date,
        pred_1day_result=result.pred_1day_result,
        pred_1day_percent=result.pred_1day_percent,
        pred_2day_result=result.pred_2day_result,
        pred_2day_percent=result.pred_2day_percent,
        pred_3day_result=result.pred_3day_result,
        pred_3day_percent=result.pred_3day_percent,
        pred_4day_result=result.pred_4day_result,
        pred_4day_percent=result.pred_4day_percent,
        pred_5day_result=result.pred_5day_result,
        pred_5day_percent=result.pred_5day_percent,
        pred_6day_result=result.pred_6day_result,
        pred_6day_percent=result.pred_6day_percent,
        pred_7day_result=result.pred_7day_result,
        pred_7day_percent=result.pred_7day_percent,
    )


@router.post("/auth/kakao", tags=["login"])
async def kakao_login(code: str = Body(..., embed=True)):
    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"
    
    payload = {
        "grant_type": "authorization_code",
        "client_id": '9e848430d64c21d951929df1b19f8617',  # 카카오 REST API 키
        "redirect_uri": 'http://localhost:4142/login-kakao',  # 카카오 개발자 설정에 등록한 리다이렉트 URI
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
                
        return_info = {'kakao_id': kakao_id, 'nickname': nickname}

        return return_info

@router.get("/user/info/{user_id}", response_model=UserInfoResponse)
async def get_user_info(user_id: int):
    with Session(engine) as session:
        result = session.query(UserInfo).filter(UserInfo.id == user_id).first()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return result