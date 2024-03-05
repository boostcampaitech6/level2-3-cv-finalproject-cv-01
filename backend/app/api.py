from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from .schemas import PredictionRequest, PredictionResponse
from .database import PredictionResult, engine
from model import get_CNN5d_5d,get_CNN5d_20d,get_CNN20d_5d,get_CNN20d_20d, inference
from utils import get_stock_data

router = APIRouter()


@router.post("/stock", tags=["stock"])
async def stock_df(stock_info: PredictionRequest):
    df = get_stock_data(stock_info.name, stock_info.period, stock_info.interval)
    return df.to_json(orient="records")

@router.post("/pred/cnn", tags=["predict"])
def pred_cnn(stock_info: PredictionRequest)->PredictionResponse:

    src_window = 5
    df = get_stock_data(stock_info.name, '1mo', '1d') # period: 1mo, interval: 1d
    df = df.iloc[-src_window:]
    model = get_CNN5d_5d()

    pred = inference(model, df, src_window)

    # 예측 결과를 DB에 저장
    prediction_result = PredictionResult(result=pred['percentage'])
    with Session(engine) as session:
        session.add(prediction_result)
        session.commit()
        session.refresh(prediction_result)
    
    return PredictionResponse(id=prediction_result.id, result=pred["percentage"])

@router.get("/pred/cnn")
def get_predictions() -> list[PredictionResponse]:
    with Session(engine) as session:
        statement = select(PredictionResult)
        prediction_results = session.exec(statement).all()
        return [
            PredictionResponse(id=prediction_result.id, result=prediction_result.result)
            for prediction_result in prediction_results
        ]

@router.get("/pred/cnn/{id}")
def get_preidction(id: int) -> PredictionResponse:
    with Session(engine) as session:
        prediction_result = session.get(PredictionResult, id)
        if not prediction_result:
            raise HTTPException(
                detail="Not found", status_code=status.HTTP_404_NOT_FOUND
            )
        return PredictionResponse(
            id=prediction_result.id, result=prediction_result.result
        )