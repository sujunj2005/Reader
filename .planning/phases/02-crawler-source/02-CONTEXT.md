# Phase 2 Context: Novel Source Management (Crawler)

## Domain Boundary

This phase delivers the crawling system for the novel reader website:
- Novel data models (novel, chapter, content, source metadata)
- Crawler engine (requests + BeautifulSoup)
- Incremental crawling logic (track scraped chapters)
- Anti-scraping strategies (User-Agent rotation, request delay, optional proxy)
- Source configuration management (admin UI for adding/editing sources)
- Scheduled task scheduling (APScheduler)
- Manual trigger for specific sources

## Decisions

### Crawler Target Strategy

- **Dual support**: Built-in rules for known novel websites + user-customizable rules
- **Built-in sources**: Common novel sites like Biquge with pre-configured CSS selectors/XPath
- **Custom sources**: Admin can add arbitrary sites with configurable:
  - Base URL pattern
  - Novel list page selector
  - Chapter list selector  
  - Content selector
  - Title/metadata extraction rules

### Anti-Scraping Strategy

- **Medium intensity**: User-Agent rotation + request delay + optional proxy pool
- **User-Agent pool**: Multiple common browser User-Agent strings, rotated per request
- **Request delay**: Configurable delay between requests (default 1-3 seconds)
- **Proxy support**: Optional proxy pool configuration via environment variables
- **Retry logic**: Configurable retry count with exponential backoff

### Data Storage Granularity

- **Full storage**: Novel metadata + chapters + full content + source + crawl status
- **Novel table**: id, title, author, description, source_url, cover_image, status, created_at, updated_at
- **Chapter table**: id, novel_id, chapter_number, title, url, content (text), crawled_at, status
- **Source table**: id, name, base_url, config (JSON), enabled, last_crawled_at
- **Crawl job table**: id, source_id, status, started_at, completed_at, chapters_crawled, chapters_total

### Crawler Architecture

- **Modular design**: Base crawler class + site-specific implementations
- **Incremental logic**: Track crawled chapters by URL or content hash to avoid duplicates
- **Job queue**: Crawl jobs managed via database records with status tracking
- **Async support**: Use asyncio with aiohttp for concurrent chapter fetching (optional)

## Canonical Refs

- `.planning/PROJECT.md` — Project context and goals
- `.planning/REQUIREMENTS.md` — CONT-01, CONT-02, CONT-03, CONT-06
- `.planning/ROADMAP.md` — Phase 2 definition and success criteria
- `.planning/phases/01-infrastructure-auth/01-CONTEXT.md` — Prior phase decisions (database, auth)

## Code Context

- Phase 1 completed: FastAPI backend, PostgreSQL, SQLAlchemy async, Alembic, JWT auth
- Database: `backend/src/database.py` with async engine and Base model
- Config: `backend/src/config.py` with Pydantic Settings

## Scope Boundaries

**In Scope for Phase 2:**
- Novel and chapter data models
- Crawler engine with base class
- Built-in crawler for at least 1 common novel site
- Custom crawler configuration system
- Incremental crawling with duplicate detection
- Anti-scraping strategies (User-Agent, delay, proxy)
- Crawl job management (start, pause, status tracking)
- Scheduled crawling via APScheduler
- Manual trigger endpoint

**Out of Scope for Phase 2 (deferred to later phases):**
- File import functionality (Phase 3)
- Reading experience (Phase 4)
- Translation module (Phase 6)

## Success Criteria (from ROADMAP.md)

1. Admin can configure crawler target websites
2. System incrementally crawls novel content on schedule
3. User can manually trigger crawling for specific sources
4. Crawler data correctly stored and associated with novel metadata

## Deferred Ideas

(None identified during discussion)

---
*Last updated: 2026-04-27 after Phase 2 discussion*
