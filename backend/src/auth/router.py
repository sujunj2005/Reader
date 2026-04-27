from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .schemas import UserCreate, UserLogin, UserResponse, TokenResponse, PasswordReset, PasswordResetConfirm
from .service import create_user, authenticate_user, get_user_by_email
from .utils import create_access_token, create_refresh_token
from .dependencies import get_current_user
from .models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await create_user(db, user_data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(db: AsyncSession = Depends(get_db)):
    # In production, refresh token should be passed via httpOnly cookie
    # Simplified implementation for now
    pass


@router.post("/password-reset")
async def request_password_reset(data: PasswordReset, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, data.email)
    if user:
        # Send password reset email (to be implemented later)
        pass
    return {"message": "If email exists, reset instructions have been sent"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
