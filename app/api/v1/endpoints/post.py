from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.crud.post import create_post, delete_post, get_post, get_posts, update_post
from app.models import User
from app.schema.post import PostCreate, PostRead, PostUpdate

router = APIRouter()


@router.get("/", response_model=List[PostRead])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_posts(db, skip, limit)

@router.get("/{post_id}", response_model=PostRead)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return db_post

@router.post("/", response_model=PostRead, status_code=201)
def create_new_post(post_in: PostCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_post(db, user.id, post_in)

@router.put("/{post_id}", response_model=PostRead)
def update_existing_post(post_id: int, post_in: PostUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if db_post.user_id != user.id or user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions")
    
    return update_post(db=db, db_post=db_post, post_in=post_in)
