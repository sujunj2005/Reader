from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SourceBase(BaseModel):
    name: str
    base_url: str
    config: dict = {}
    enabled: bool = True


class SourceCreate(SourceBase):
    pass


class SourceResponse(SourceBase):
    id: str
    created_at: datetime
    updated_at: datetime
    last_crawled_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NovelBase(BaseModel):
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
    source_url: str
    cover_image: Optional[str] = None
    status: str = "ongoing"


class NovelResponse(NovelBase):
    id: str
    source_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChapterBase(BaseModel):
    chapter_number: int
    title: str
    url: str
    content: Optional[str] = None
    status: str = "pending"


class ChapterResponse(ChapterBase):
    id: str
    novel_id: str
    crawled_at: datetime

    class Config:
        from_attributes = True


class CrawlJobResponse(BaseModel):
    id: str
    source_id: str
    status: str
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    chapters_crawled: int
    chapters_total: int
    error_message: Optional[str] = None

    class Config:
        from_attributes = True
