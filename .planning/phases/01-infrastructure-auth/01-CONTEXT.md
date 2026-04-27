# Phase 1 Context: Infrastructure & Authentication

## Domain Boundary

This phase delivers the foundational architecture for the novel reader website:
- Python FastAPI backend framework
- PostgreSQL database configuration
- JWT-based authentication system with OAuth2.0 flow
- Vue 3 frontend project scaffold
- Docker Compose deployment configuration
- User registration, login, logout, and password reset functionality

## Decisions

### Database

- **Selection**: PostgreSQL
  - Rationale: Multi-user support needed for potential future public release
  - Better concurrency than SQLite for production workloads
  - Strong security and governance features
  - Compatible with FastAPI ecosystem

- **ORM**: SQLAlchemy
  - Rationale: Most mature Python ORM, excellent FastAPI integration
  - Supports async operations for better performance
  - Easy migration path for future scaling

### Authentication Strategy

- **Token Type**: JWT (JSON Web Tokens)
- **Flow**: OAuth2.0 with OAuth2PasswordBearer (FastAPI standard)
- **Token Strategy**: Access Token + Refresh Token
  - Access Token: 15 minutes expiry
  - Refresh Token: 7 days expiry
  - Secure logout via token invalidation
- **Password Hashing**: bcrypt with salt
- **Login Method**: Email/password authentication

### Frontend Architecture

- **Framework**: Vue 3 with Composition API
- **Build Tool**: Vite
- **State Management**: Pinia (for auth state)
- **Routing**: Vue Router
- **HTTP Client**: Axios (for API calls)
- **UI Components**: To be decided (Element Plus or similar)

### Deployment Structure

- **Container Orchestration**: Docker Compose (multi-container)
- **Services**:
  - Backend (FastAPI + Uvicorn)
  - Frontend (Vue 3 + Nginx for production)
  - Database (PostgreSQL)
- **Environment Variables**: `.env` file for configuration
- **Volume Management**: Persistent PostgreSQL data volume

## Canonical Refs

- `.planning/PROJECT.md` — Project context and goals
- `.planning/REQUIREMENTS.md` — v1 Requirements (AUTH-01 through AUTH-04, DEPLOY-01 through DEPLOY-03)
- `.planning/ROADMAP.md` — Phase 1 definition and success criteria
- `.planning/config.json` — Project configuration

## Code Context

(No existing code — greenfield project)

## Scope Boundaries

**In Scope for Phase 1:**
- User registration with email/password
- User login with JWT token generation
- User logout with token invalidation
- Password reset functionality
- FastAPI project structure
- PostgreSQL database setup
- Vue 3 project scaffold
- Docker Compose configuration

**Out of Scope for Phase 1 (deferred to later phases):**
- Novel scraping/crawling (Phase 2)
- File import functionality (Phase 3)
- Reading experience (Phase 4)
- Book management (Phase 5)
- Translation module (Phase 6)
- User profile customization (Phase 7)

## Success Criteria (from ROADMAP.md)

1. User can successfully register and login
2. User stays logged in after page refresh
3. Docker Compose can start all services with one command
4. Environment variables can configure different AI model endpoints

## Deferred Ideas

(None identified during discussion)

---
*Last updated: 2026-04-27 after Phase 1 discussion*
