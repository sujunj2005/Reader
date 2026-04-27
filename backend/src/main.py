from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .auth.router import router as auth_router

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


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.API_VERSION}
