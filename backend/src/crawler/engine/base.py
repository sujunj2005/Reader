from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bs4 import BeautifulSoup
from ..models import Source, Novel, Chapter
from .utils import async_fetch, RateLimiter


class BaseCrawler(ABC):
    def __init__(self, source: Source, db: AsyncSession, rate_limiter: Optional[RateLimiter] = None):
        self.source = source
        self.db = db
        self.rate_limiter = rate_limiter or RateLimiter()
        self.config = source.config or {}

    @abstractmethod
    async def parse_novel_list(self, html: str) -> List[Dict]:
        pass

    @abstractmethod
    async def parse_chapter_list(self, html: str) -> List[Dict]:
        pass

    @abstractmethod
    async def parse_chapter_content(self, html: str) -> str:
        pass

    async def fetch_page(self, url: str) -> str:
        response = await async_fetch(
            url,
            proxy=self.config.get("proxy"),
            retry_count=self.config.get("retry_count", 3),
        )
        return response.text

    async def parse_html(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")

    async def crawl_chapters(self, novel: Novel) -> int:
        html = await self.fetch_page(novel.source_url)
        await self.rate_limiter.wait()
        chapters = await self.parse_chapter_list(html)

        crawled_count = 0
        for ch_info in chapters:
            existing = await self.db.execute(
                select(Chapter).where(Chapter.url == ch_info["url"])
            )
            if existing.scalar_one_or_none():
                continue

            content_html = await self.fetch_page(ch_info["url"])
            await self.rate_limiter.wait()
            content = await self.parse_chapter_content(content_html)

            chapter = Chapter(
                novel_id=novel.id,
                chapter_number=ch_info.get("chapter_number", 0),
                title=ch_info["title"],
                url=ch_info["url"],
                content=content,
                status="crawled",
            )
            self.db.add(chapter)
            crawled_count += 1

        await self.db.flush()
        return crawled_count
