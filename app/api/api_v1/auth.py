from fastapi import APIRouter, Body, Request, HTTPException,Depends
from fastapi.responses import JSONResponse, Response
from models.user import UserIn, User

from datetime import datetime
from core import security
from core.authentication import AuthHandler

auth_handler = AuthHandler()


router = APIRouter()

@router.post("/auth/register", response_description="Register a new user")
async def register_user(
    request: Request,
    newUser: UserIn = Body(...)
):
    try:
        existing_user = await User.find(User.email == newUser.email).first_or_none()
        print("printing existing user")
        if existing_user:
            raise HTTPException(status_code=409, detail="User with this email already exists")

        user = User(
            username=newUser.username,
            password=security.get_password_hash(newUser.password),
            email=newUser.email,
            created_at=datetime.utcnow()  # ✅ Correct field name
        )

        print("Inserting user:", user.dict())
        result = await user.insert()
        print("Inserted:", result)
        return {"message": "User registered successfully", "user": user.username}

    except Exception as e:
        print("Error during registration:", str(e))  # ✅ Useful for debugging
        raise HTTPException(status_code=500, detail="Internal Server Error")
        
    
    

@router.post("/auth/login", response_description="Login a user")
async def login_user(
    request: Request,
    newUser: UserIn
):
    user = None
    try:
        user = await User.find(User.email == newUser.email).first_or_none()
        print(user)
        if(user and security.verify_password(newUser.password, user.password)):
            print("trying to verify")
            jwt_token = auth_handler.encode_token(user_id=user.id)
            response = JSONResponse(content={"message": "User Logged In!"})
            response.set_cookie(
                key="access_token",
                value=jwt_token,
                httponly=True,
                samesite="lax",
                secure=False
            )
            return response
        else:
            raise HTTPException(status_code=401,detail="Invalid Credentials")
    except:
        return {"message":"Cannot login due to invalid credentials"}

@router.post("/auth/logout")
async def logout_user():
    response = Response(content="Logged out", status_code=200)
    response.delete_cookie("access_token")
    return response