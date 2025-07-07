from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schema.user import UserCreate, UserRead, UserUpdate


def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(email=user_in.email, hashed_password=hash_password(user_in.password), role=user_in.role or "user")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()

def get_user_by_email(db: Session, user_email: str) -> User | None:
    stmt = select(User).where(User.email == user_email)
    return db.execute(stmt).scalar_one_or_none()

def update_user(db: Session, db_user: User, user_in: UserUpdate):
    if user_in.email:
        db_user.email = user_in.email
    if user_in.password:
        db_user.hashed_password = hash_password(user_in.password)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()