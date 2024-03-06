from pydantic import BaseModel

class PredictionRequest(BaseModel):
    name: str

class PredictionResponse(BaseModel):
    id: int
    result: int
    percentage: float