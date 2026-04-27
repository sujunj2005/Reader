from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReadingProgressUpdate(BaseModel):
    novel_id: str
    chapter_id: str
    scroll_position: int = 0


class ReadingProgressResponse(BaseModel):
    id: str
    user_id: str
    novel_id: str
    chapter_id: str
    scroll_position: int
    updated_at: datetime

    class Config:
        from_attributes = True


class BookmarkCreate(BaseModel):
    novel_id: str
    chapter_id: str
    note: Optional[str] = None


class BookmarkResponse(BaseModel):
    id: str
    novel_id: str
    chapter_id: str
    note: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ChapterResponse(BaseModel):
    id: str
    novel_id: str
    chapter_number: int
    title: str
    content: Optional[str] = None

    class Config:
        from_attributes = True


class NovelChaptersResponse(BaseModel):
    id: str
    title: str
    author: Optional[str] = None
    chapters: list[ChapterResponse]
