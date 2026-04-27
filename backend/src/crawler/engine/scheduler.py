from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select
from datetime import datetime
from ..models import Source, Novel, CrawlJob
from .factory import get_crawler


class CrawlScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self._db_session_factory = None

    def set_db_session_factory(self, factory):
        self._db_session_factory = factory

    async def start(self):
        self.scheduler.start()

    async def shutdown(self):
        self.scheduler.shutdown()

    def add_source_job(self, source_id: str, cron_expression: str = "0 2 * * *"):
        self.scheduler.add_job(
            self._run_crawl_job,
            trigger=CronTrigger.from_crontab(cron_expression),
            args=[source_id],
            id=f"crawl_{source_id}",
            replace_existing=True,
        )

    def remove_source_job(self, source_id: str):
        job_id = f"crawl_{source_id}"
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)

    async def _run_crawl_job(self, source_id: str):
        async with self._db_session_factory() as db:
            try:
                source = (await db.execute(select(Source).where(Source.id == source_id))).scalar_one_or_none()
                if not source or not source.enabled:
                    return

                crawler = get_crawler(source, db)
                if not crawler:
                    return

                job = CrawlJob(
                    source_id=source_id,
                    status="running",
                    started_at=datetime.utcnow(),
                )
                db.add(job)
                await db.flush()

                novels = (await db.execute(select(Novel).where(Novel.source_id == source_id))).scalars().all()
                total_crawled = 0

                for novel in novels:
                    crawled = await crawler.crawl_chapters(novel)
                    total_crawled += crawled

                source.last_crawled_at = datetime.utcnow()
                job.status = "completed"
                job.completed_at = datetime.utcnow()
                job.chapters_crawled = total_crawled
                await db.commit()

            except Exception as e:
                await db.rollback()
                import traceback
                traceback.format_exc()
                job.status = "failed"
                job.error_message = str(e)[:2000]
                await db.commit()


scheduler = CrawlScheduler()
