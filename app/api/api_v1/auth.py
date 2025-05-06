from fastapi import APIRouter, Body, Request
from models.user import UserIn, User
from datetime import datetime

router = APIRouter()

@router.post("/auth/register",response_description="Resgister a new user",)
async def register_user(
    request: Request,
    newUser: UserIn = Body(...)
):
    user = User(username=newUser.username, password=newUser.password, email=newUser.email, createdAt=datetime.utcnow)
    print("Inserting user:", user.dict())
    result = await user.insert()
    print("Inserted:", result)
    return {"message":"Register User",
            "newUser":newUser}

@router.post("/auth/login")
async def register_user():
    return {"message":"Login User"}

@router.post("/auth/logout")
async def register_user():
    return {"message":"Logout User"}