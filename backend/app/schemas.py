from pydantic import BaseModel

class UserInfoResponse(BaseModel):
    id: int
    created_at: str

class FavoriteStocksResponse(BaseModel):
    user_id: int
    stock_code: int

class KRXResponse(BaseModel):
    code: str 
    name: str
    market: str
    close: str