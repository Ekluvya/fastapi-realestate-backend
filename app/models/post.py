from pydantic import Field, BaseModel
from uuid import UUID, uuid4
from beanie import Document, Indexed
from datetime import datetime
from enum import Enum
from typing import Optional, List, Annotated

class PropertyType(str, Enum):
    apartment = 'apartment'
    house = 'house'
    condo = 'condo'
    land = 'land'

class ContractType(str, Enum):
    buy = 'buy'
    rent = 'rent'

class PostDetail(BaseModel):
    id: UUID= Field(default_factory=uuid4)
    desc:str = Field(...)
    images:List[str] = Field(default_factory=list)
    utilities: Optional[str] = Field(...)
    pet: Optional[str] = Field(...)
    income: Optional[str] = Field(...)
    size: Optional[int] = Field(...)
    school: Optional[int] = Field(...)
    bus: Optional[int] = Field(...)
    restaurant: Optional[int] = Field(...)
    
class Post(Document):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(...)
    price: int = Field(...)
    img: str = Field(default_factory=str)
    address: str = Field(...)
    city: Annotated[str, Indexed()] = Field(...)
    bedroom: int = Field(...)
    bathroom: int = Field(...)
    latitude: float = Field(...)
    longitude: float = Field(...)
    p_type: PropertyType = Field(...)
    c_type: ContractType = Field(...)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[UUID] = None
    postDetail: PostDetail

    class Settings:
        name = "posts"
        use_revision = True  # Enable document revision tracking



