from fastapi import FastAPI

from app.api.v1.routers import api_router

app = FastAPI(
    title="My FastAPI Project",
    description="API Documentation",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")
