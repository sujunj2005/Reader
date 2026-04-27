from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .auth.router import router as auth_router
from .crawler.router import router as crawler_router
from .crawler.engine.scheduler import scheduler
from .database import async_session_maker

settings = get_settings()

app = FastAPI(
    title=settings.API_NAME,
    version=settings.API_VERSION,
    debug=settings.API_DEBUG,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(crawler_router)


@app.on_event("startup")
async def startup_event():
    scheduler.set_db_session_factory(async_session_maker)
    await scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    await scheduler.shutdown()


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.API_VERSION}
