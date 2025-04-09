from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserPublic(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    title: str
    slug: str
    content: str
    tags: Optional[str] = None


class PostOut(PostCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    user: UserPublic

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        orm_mode = True

class PaginatedPosts(BaseModel):
    total: int
    posts: list[PostOut]


