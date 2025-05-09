from uuid import uuid4
from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# -------------------------
# Define models inline (or import from your app)
# -------------------------

class PostDetail(BaseModel):
    desc: str
    images: List[str] = Field(default_factory=list)
    utilities: Optional[str]
    pet: Optional[str]
    income: Optional[str]
    size: Optional[int]
    school: Optional[int]
    bus: Optional[int]
    restaurant: Optional[int]

class Post(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    price: int
    img: str
    address: str
    city: str
    bedroom: int
    bathroom: int
    latitude: float
    longitude: float
    p_type: str
    c_type: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    postDetail: PostDetail

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    username: str
    password: str
    email: EmailStr
    avatar: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    posts: List[Post] = Field(default_factory=list)

# -------------------------
# Simulate logic
# -------------------------

def main():
    # Create user
    user = User(
        username="testuser",
        password="hashedpass",
        email="test@example.com",
    )

    print("User created:")
    print(user)

    # Create post detail
    detail = PostDetail(
        desc="Nice 2BHK apartment in city center",
        images=["img1.jpg", "img2.jpg"],
        utilities="Water, Gas",
        pet="Yes",
        income="3x rent",
        size=1200,
        school=5,
        bus=2,
        restaurant=4
    )

    # Create post linked to user
    post = Post(
        title="2BHK Central",
        price=2000,
        img="main.jpg",
        address="456 City Road",
        city="Metroville",
        bedroom=2,
        bathroom=2,
        latitude=12.9716,
        longitude=77.5946,
        p_type="apartment",
        c_type="rent",
        user_id=user.id,
        postDetail=detail
    )

    print("\nPost created:")
    print(post)

    # Link post to user manually
    user.posts.append(post)

    print("\nUser after adding post:")
    print(user)

    print("\nAccessing user's first post title:", user.posts[0].title)

if __name__ == "__main__":
    main()
