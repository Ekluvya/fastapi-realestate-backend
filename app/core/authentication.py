import os
from fastapi import Request
from dotenv import load_dotenv
import datetime
import jwt
from uuid import UUID, uuid4
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.user import User, UserOut


class AuthHandler:
    http_security = HTTPBearer()
    secret = os.getenv("JWT_SECRET","default-secret-for-dev")
    token_expiry_time = int(os.getenv("TOKEN_EXPIRY_MINUTES",30))

    def encode_token(self, user_id:uuid4) -> str:
        payload = {
            "exp":datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=self.token_expiry_time),
            "iat":datetime.datetime.now(datetime.timezone.utc),
            "user_id":str(user_id),
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")
    
    def decode_token(self, request:Request):
        token = request.cookies.get("access_token")
        if not token:
             raise HTTPException(status_code=401, detail="Not Authenticated")
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if "user_id" not in payload:
                raise HTTPException(status_code=401, detail="Invalid token payload")
            return {"user_id":str(payload["user_id"])}
        except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")
    
    async def get_current_user(self, request: Request):
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Not Authenticated")
        
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            id = UUID(payload["user_id"])

            if not id:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            user = await User.find(User.id == id).first_or_none()
            print("printing user after login in:", user)

            if not user:
                raise HTTPException(status_code=401, detail="User not found")

            return UserOut(username=user.username, avatar=user.avatar, email=user.email)

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(http_security)):
        if not auth.credentials:
            raise HTTPException(status_code=401, detail="No token provided")
        return self.decode_token(auth.credentials)
         



