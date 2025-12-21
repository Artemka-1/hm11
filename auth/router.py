from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas import UserCreate, UserResponse, Token
from app.models import User
from app.security import hash_password, verify_password, create_token
from app.deps import get_db
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201, response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")

    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_token(
        {"sub": str(db_user.id)},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh = create_token(
        {"sub": str(db_user.id)},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access,
        "refresh_token": refresh
    }
