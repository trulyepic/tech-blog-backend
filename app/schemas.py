from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    slug: str
    content: str
    tags: Optional[str] = None


class PostOut(PostCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
