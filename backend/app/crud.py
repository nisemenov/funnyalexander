import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app import models, schemas
from app.api.deps import SessionDep, TokenDep, pwd_context


# USER

def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    return db.get(models.User, user_id)

def get_user_by_email(db: Session, email) -> models.User | None:
    model = models.User
    return db.scalar(select(model).filter(model.email == email))

def get_user_by_username(db: Session, username) -> models.User | None:
    return db.scalar(select(models.User).where(models.User.username == username))

def get_users(db:Session, skip: int = 0, limit: int = 100) -> Session.query:
    return db.scalars(select(models.User)).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    user_dict = user.model_dump()
    hashed_password = get_password_hash(user_dict.pop('password'))
    db_user = models.User(
        **user_dict,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Item
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(
    db: Session, item: schemas.ItemCreate, user_id: int
) -> models.Item:
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# LOGIN

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: SessionDep, username: str, password: str):
    db_user = get_user_by_username(db, username)
    if not db_user:
        return None
    if not pwd_context.verify(password, db_user.hashed_password):
        return None
    return db_user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(
    db: SessionDep, token: TokenDep
) -> models.User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        # token_data = schemas.TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)],
) -> models.User | None:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
