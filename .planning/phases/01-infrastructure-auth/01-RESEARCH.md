# Phase 1 Research: Infrastructure & Authentication

## FastAPI Project Structure

**Recommended Structure** (based on Netflix Dispatch pattern):
```
backend/
├── alembic/              # Database migrations
├── src/
│   ├── auth/             # Authentication module
│   │   ├── router.py     # Auth endpoints
│   │   ├── schemas.py    # Pydantic models
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── service.py    # Business logic
│   │   ├── dependencies.py
│   │   └── utils.py
│   ├── config.py         # Global config (Pydantic BaseSettings)
│   ├── database.py       # DB connection
│   ├── models.py         # Global models
│   └── main.py           # App entry point
├── tests/
│   └── auth/
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env.example
└── Dockerfile
```

**Key Patterns:**
- Domain-based module organization (auth, users, etc.)
- SQLAlchemy ORM with async support
- Pydantic for data validation
- Alembic for database migrations
- Environment-based configuration via Pydantic BaseSettings

## JWT Authentication

**Best Practice Stack:**
- **Library**: `python-jose` for JWT + `passlib[bcrypt]` for password hashing
- **Flow**: OAuth2PasswordBearer with httpOnly cookies for token storage
- **Token Strategy**: Access Token (15min) + Refresh Token (7 days)
- **Security**: 
  - bcrypt password hashing with salt rounds >= 12
  - httpOnly cookies to prevent XSS
  - SameSite=Strict cookie attribute
  - HTTPS in production

**FastAPI Auth Pattern:**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    # Decode and validate token
```

## PostgreSQL + SQLAlchemy

**Configuration:**
- Use `psycopg2-binary` or `asyncpg` for PostgreSQL driver
- SQLAlchemy 2.0 with async engine (`create_async_engine`)
- Connection pooling with `AsyncSession`
- Alembic for migrations

**Naming Convention** (important for migrations):
```python
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
```

## Docker Compose Setup

**Services:**
1. **backend** - FastAPI + Uvicorn
2. **frontend** - Vue 3 + Nginx (production) / Vite dev server
3. **db** - PostgreSQL 15+
4. **redis** (optional for caching/sessions)

**docker-compose.yml Pattern:**
```yaml
version: '3.8'
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: novel_reader
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:${DB_PASSWORD}@db:5432/novel_reader
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

## Vue 3 Frontend Architecture

**Recommended Stack:**
- Vue 3 + Composition API
- Vite (build tool)
- Vue Router (routing)
- Pinia (state management)
- Axios (HTTP client)
- Element Plus or Naive UI (component library)

**Auth Flow:**
1. User submits login form
2. Backend returns JWT in httpOnly cookie
3. Pinia stores user info (not token)
4. Axios interceptors handle auth state
5. Router guards protect authenticated routes

## Key Dependencies

**Backend:**
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
asyncpg>=0.29.0
alembic>=1.12.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-multipart>=0.0.6
python-dotenv>=1.0.0
```

**Frontend:**
```
vue@^3.3.0
vue-router@^4.2.0
pinia@^2.1.0
axios@^1.6.0
@vitejs/plugin-vue@^4.5.0
vite@^5.0.0
```

---
*Research completed: 2026-04-27*
