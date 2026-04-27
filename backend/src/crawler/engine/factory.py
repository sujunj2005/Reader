from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Source
from .base import BaseCrawler
from .biquge import BiqugeCrawler

CRAWLER_REGISTRY = {
    "biquge": BiqugeCrawler,
}


def get_crawler(source: Source, db: AsyncSession) -> Optional[BaseCrawler]:
    crawler_type = source.config.get("type", "biquge")
    crawler_class = CRAWLER_REGISTRY.get(crawler_type)

    if crawler_class:
        return crawler_class(source=source, db=db)

    return None


def register_crawler(crawler_type: str, crawler_class: type):
    CRAWLER_REGISTRY[crawler_type] = crawler_class
