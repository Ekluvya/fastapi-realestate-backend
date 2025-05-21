from fastapi import APIRouter, Depends, HTTPException
from core.authentication import AuthHandler
from models.user import UserUpdate, User, UserOut
from models.post import Post
from uuid import UUID
from core import security
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

auth_handler = AuthHandler()

router = APIRouter()

@router.get("/user/me", response_description="for getting current user details")
async def me(current_user= Depends(auth_handler.get_current_user)):
    return current_user.model_dump()

@router.put("/user/update", response_description="for updating current user details",)
async def me(newUserDetails: UserUpdate,current_user_id= Depends(auth_handler.decode_token),):
    user_id = current_user_id["user_id"]

    #Find user by ID
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, details="User not found")
    
    if newUserDetails.username:
        user.username = newUserDetails.username
    if newUserDetails.email:
        user.email = newUserDetails.email
    if newUserDetails.password:
        user.password = security.get_password_hash(newUserDetails.password)
    if newUserDetails.avatar:
        user.avatar = newUserDetails.avatar

    await user.save()
    return UserOut(username=user.username, email=user.email, avatar=user.avatar)

@router.get("/user/get_user/{id}", response_description="for updating current user details",)
async def get_user(id:str, current_user_id= Depends(auth_handler.decode_token),):
    if not current_user_id:
        raise HTTPException(status_code=404, details="User not found")
    
    find_id = UUID(id)
    user = await User.get(find_id)

    user_json = jsonable_encoder(UserOut(username=user.username, email=user.email, avatar=user.avatar))
    return JSONResponse(content=user_json)

@router.get("/user/get-saved-items")
async def get_saved_posts(user_id= Depends(auth_handler.decode_token)):
    if not user_id:
        raise HTTPException(status_code=401,detail="User not found")
    user = await User.get(UUID(user_id["user_id"]))
    await user.fetch_link("saved_posts")
    saved_posts = user.saved_posts

    saved_json_posts = jsonable_encoder(saved_posts)
    return JSONResponse(content=saved_json_posts)

@router.get("/user/get-created-items")
async def get_saved_posts(user_id= Depends(auth_handler.decode_token)):
    if not user_id:
        raise HTTPException(status_code=401,detail="User not found")
    user = await User.get(UUID(user_id["user_id"]))
    created_posts = await Post.find(Post.user_id == user.id).to_list()
    created_posts_json = jsonable_encoder(created_posts)

    
    return JSONResponse(content=created_posts_json)