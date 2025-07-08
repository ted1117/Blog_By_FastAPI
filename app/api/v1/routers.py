from fastapi import APIRouter

from app.api.v1.endpoints import auth, comment, item, post

api_router = APIRouter()


api_router.include_router(auth.router, prefix="/users", tags=["users"])
api_router.include_router(post.router, prefix="/posts", tags=["posts"])
api_router.include_router(comment.router, prefix="/comments", tags=["comments"])