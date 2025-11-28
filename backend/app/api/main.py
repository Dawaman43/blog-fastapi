from fastapi import APIRouter

from app.api.routes.admin import router as admin_router
from app.api.routes.auth import router as auth_router
from app.api.routes.blogs import router as blog_router

api = APIRouter()

api.include_router(blog_router)
api.include_router(admin_router)
api.include_router(auth_router)
