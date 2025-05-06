from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.api_v1.auth import router as auth_router
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import BaseConfig
from beanie import init_beanie
from models.user import User

settings = BaseConfig()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Up!")
    client = AsyncIOMotorClient(settings.DB_URL)
    
    try:
        await init_beanie(database=client.real_estate, document_models=[User])
        print("Pinged your deployment. You have successfully connected to MongoDB!")
        print("Mongo address:", settings.DB_URL)
    except Exception as e:
        print(e)

    yield
    print("Shutting Down!")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth_router,prefix="/api",tags=["auth"])