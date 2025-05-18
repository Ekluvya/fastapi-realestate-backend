from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link
from datetime import datetime
from typing import Optional, List, Annotated

from models.post import Post


class User(Document):
    id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)
    username: str = Field(..., min_length=3, max_length=15)
    password: str = Field(...)
    email: Annotated[EmailStr, Indexed()] = Field(...)
    avatar: Optional[str] = None  # You can keep it optional
    created_at: datetime = Field(default_factory=datetime.utcnow)
    saved_posts: List[Link[Post]] = Field(default_factory=list)

    class Settings:
        name = "users"
        user_revision: True

class UserIn(BaseModel):
    username: Optional[str] = None
    password: str = Field(...)
    email: Optional[EmailStr] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None

# Output model to return safe user data
class UserOut(BaseModel):
    username: str
    email: EmailStr
    avatar: Optional[str]


    class Config:
        orm_mode = True  # Needed to convert Beanie documents to Pydantic


