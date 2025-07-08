from fastapi import APIRouter

from app.api.v1.endpoints import auth, post

api_router = APIRouter()


api_router.include_router(auth.router, prefix="/users", tags=["users"])
api_router.include_router(post.router, prefix="/posts", tags=["posts"])