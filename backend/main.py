from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger 
from sqlmodel import SQLModel

# from app.config import config
from app.database import engine
from app.api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("creating database table")
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)