from fastapi import APIRouter, Depends, HTTPException
from core.authentication import AuthHandler
from models.user import UserUpdate, User, UserOut
from core import security

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