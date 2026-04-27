# Phase 1 Discussion Log

## Session Info

**Phase:** 01 — Infrastructure & Authentication  
**Date:** 2026-04-27  
**Mode:** Default (interactive)

## Areas Discussed

### 1. Database Selection

**Options Presented:**
- PostgreSQL (Recommended) — Production-grade database, supports multi-user concurrency, scalable for future public release
- SQLite — Zero configuration, single file, suitable for personal use and small deployments
- User has specific preferences

**User Decision:** PostgreSQL (Recommended)

**Notes:**
- Selected for future multi-user support
- Better concurrency than SQLite
- Compatible with FastAPI ecosystem

### 2. Authentication Strategy

**Options Presented:**
- httpOnly Cookie (Recommended) — More secure, XSS protection, suitable for SPA + API architecture
- localStorage + Authorization Header — Simpler but XSS vulnerable
- User has specific preferences

**User Input:** "使用JWT的token，使用Oauth2.0的流程" (Use JWT token with OAuth2.0 flow)

**Additional Decision — Token Refresh Strategy:**

**Options Presented:**
- Access + Refresh Token (Recommended) — Short Access token (15min) + long Refresh token (7 days), secure with good UX
- Single Token with long expiry — Simpler but less secure

**User Decision:** Access + Refresh Token (Recommended)

**Notes:**
- JWT + OAuth2.0 flow with OAuth2PasswordBearer
- Access Token: 15 minutes
- Refresh Token: 7 days
- Password hashing with bcrypt

## Deferred Ideas

(None identified during discussion)

---
*Discussion log generated automatically from phase 1 discussion*
