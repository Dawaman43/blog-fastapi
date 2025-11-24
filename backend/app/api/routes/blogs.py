from fastapi import APIRouter


router = APIRouter(prefix="/blogs", tags=["tags"])


@router.get("/")
