from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.api_v1.auth import router as auth_router
from api.api_v1.users import router as user_router
from api.api_v1.post import router as post_router
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import BaseConfig
from beanie import init_beanie
from models.user import User
from models.post import Post
from bson.binary import UuidRepresentation

settings = BaseConfig()
origins = ["http://localhost:5173"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Up!")
    client = AsyncIOMotorClient(settings.DB_URL,uuidRepresentation="standard")

    
    try:
        await init_beanie(database=client.real_estate, document_models=[User,Post])
        print("Pinged your deployment. You have successfully connected to MongoDB!")
        print("Mongo address:", settings.DB_URL)
        # Resolve forward references *after* Beanie initialization
        # Update forward references after Beanie initialization
        User.update_forward_refs()
        Post.update_forward_refs()
    except Exception as e:
        print(e)

    yield
    print("Shutting Down!")


app = FastAPI(lifespan=lifespan)



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth_router,prefix="/api",tags=["auth"])
app.include_router(user_router,prefix="/api",tags=["user"])
app.include_router(post_router,prefix="/api",tags=["post"])