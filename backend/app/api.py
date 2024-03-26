from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from .schemas import UserInfoResponse, FavoriteStocksResponse, KRXResponse, CNNPredResponse, TimeSeriesPredResponse, BertPredResponse, CandlePredResponse
from .database import UserInfo, FavoriteStocks, KRX, CNNPredHistory, TimeSeriesPredHistory, BertPredHistory, CandlePredHistory, engine

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
        

@router.get("/stockinfo", tags=["stock"])
def get_stock_info() -> list[KRXResponse]:
    with Session(engine) as session:
        statement = select(KRX)
        results = session.exec(statement).all()
        return [
            KRXResponse(stock_code=result.code, stock_name=result.name, market=result.market)
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
def get_lstm_pred() -> list[BertPredResponse]:
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