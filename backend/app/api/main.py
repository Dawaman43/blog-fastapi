from fastapi import APIRouter
from routes.blogs import router as blog_router
from routes.admin import router as admin_router

api = APIRouter()

api.include_router(blog_router)
api.include_router(admin_router)
