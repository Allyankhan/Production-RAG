from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status
)

from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from app.auth.Real_user import User
from app.auth.security import (
    create_access_token,
    verify_password
)
from app.auth.service import create_user
from app.database.db import get_db

from app.models.user_login_schema import (
    LoginRequest,
    RegisterRequest
)

router = APIRouter()


@router.post(
    "/login",
    dependencies=[
        Depends(RateLimiter(times=5, seconds=60))
    ]
)
def login(
    request: Request,
    payload: LoginRequest,
    db: Session = Depends(get_db)
):
    # Find user
    user = (
        db.query(User)
        .filter(User.username == payload.username)
        .first()
    )

    # Verify credentials
    if user is None or not verify_password(
        payload.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Generate JWT
    token = create_access_token(
        {
            "sub": user.username
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post(
    "/register",
    dependencies=[
        Depends(RateLimiter(times=5, seconds=60))
    ]
)
def register(
    request: Request,
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):
    user = create_user(
        db=db,
        username=payload.username,
        email=payload.email,
        password=payload.password
    )

    return {
        "message": "User registered successfully",
        "username": user.username
    }