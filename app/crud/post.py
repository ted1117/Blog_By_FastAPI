from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schema.post import PostCreate, PostUpdate


def create_post(db: Session, user_id: int, post_in: PostCreate) -> Post:
    db_post = Post(
        title=post_in.title,
        content=post_in.content,
        user_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db: Session, post_id: int) -> Post | None:
    stmt = select(Post).where(Post.id == post_id)
    return db.execute(stmt).scalar_one_or_none()

def get_posts(db: Session, skip: int = 0, limit: int = 10) -> Sequence[Post]:
    stmt = select(Post).offset(skip).limit(limit).order_by(Post.id.desc())
    return db.execute(stmt).scalars().all()

def update_post(db: Session, db_post: Post, post_in: PostUpdate) -> Post:
    if post_in.title is not None:
        db_post.title = post_in.title
    if post_in.content is not None:
        db_post.content = post_in.content

    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, db_post: Post):
    db.delete(db_post)
    db.commit()