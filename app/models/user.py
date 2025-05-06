from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from beanie import Document
from datetime import datetime
from typing import Optional

class User(Document):
    id: UUID = Field(default_factory=uuid4)
    username: str = Field(..., min_length=3, max_length=15)
    password: str = Field(...)
    email: EmailStr = Field(...)
    avatar: Optional[str] = None  # You can keep it optional
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

class UserIn(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=15
    )
    password: str = Field(...)
    email: Optional[EmailStr] = None

# Output model to return safe user data
class UserOut(BaseModel):
    id: str
    username: str

    class Config:
        orm_mode = True  # Needed to convert Beanie documents to Pydantic