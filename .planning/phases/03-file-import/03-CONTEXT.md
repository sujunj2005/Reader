# Phase 3 Context: Novel Source Management (File Import)

## Domain Boundary

This phase delivers the file import system for the novel reader website:
- File upload endpoint with format validation
- TXT file parser with automatic encoding detection (UTF-8, GBK)
- EPUB file parser using ebooklib or similar library
- Smart chapter splitting based on patterns (empty lines, chapter headings)
- Metadata extraction (title, author from filename or content)
- Server-side file storage with database metadata tracking
- Import management UI (admin view)

## Decisions

### File Formats

- **TXT**: UTF-8/GBK auto-detection using chardet library
- **EPUB**: Using ebooklib library for parsing

### Chapter Recognition

- **Smart splitting**: Pattern-based chapter detection
  - Chapter headings like "第X章", "Chapter X", "第X节"
  - Empty line separation
  - Configurable patterns per source type

### Storage Location

- **Server-side storage**: Files stored on server disk, database tracks metadata
- **Storage path**: `./data/uploads/{novel_id}/{chapter_id}.txt`
- **Database**: Novel record + Chapter records with file path references
- **Content caching**: Extracted text stored in DB for fast reading, original file kept for reference

### Architecture

- **Importer base class**: Common interface for different format parsers
- **TXT Importer**: Encoding detection + smart chapter splitting
- **EPUB Importer**: ebooklib parsing + TOC extraction
- **Import job tracking**: Similar to CrawlJob but for file imports

## Canonical Refs

- `.planning/PROJECT.md` — Project context and goals
- `.planning/REQUIREMENTS.md` — CONT-04, CONT-05
- `.planning/ROADMAP.md` — Phase 3 definition
- `.planning/phases/02-crawler-source/02-CONTEXT.md` — Prior crawler decisions (Novel model)

## Code Context

- Phase 1: FastAPI + PostgreSQL + JWT auth
- Phase 2: Crawler system with Novel, Chapter, Source models
- Novel model already has: id, source_id, title, author, description, source_url
- Chapter model already has: id, novel_id, chapter_number, title, url, content, status

## Scope Boundaries

**In Scope for Phase 3:**
- File upload API with validation
- TXT parser with encoding detection
- EPUB parser
- Smart chapter splitting
- Metadata extraction
- Import job tracking
- Import management API

**Out of Scope for Phase 3 (deferred to later phases):**
- Reading experience (Phase 4)
- Translation module (Phase 6)

## Success Criteria (from ROADMAP.md)

1. User can upload TXT, EPUB novel files
2. System correctly parses file metadata (title, author, chapters)
3. Imported novels can be viewed and managed in bookshelf

## Deferred Ideas

(None identified during discussion)

---
*Last updated: 2026-04-27 after Phase 3 discussion*
