from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TagResponse(BaseModel):
    id: str
    name: str
    category: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class NovelSearchResult(BaseModel):
    id: str
    title: str
    author: Optional[str]
    description: Optional[str]
    cover_image: Optional[str]
    status: str

    class Config:
        from_attributes = True


class UserNovelCreate(BaseModel):
    novel_id: str
    status: str = "reading"


class UserNovelUpdate(BaseModel):
    status: str


class UserNovelResponse(BaseModel):
    id: str
    user_id: str
    novel_id: str
    status: str
    added_at: datetime

    class Config:
        from_attributes = True
