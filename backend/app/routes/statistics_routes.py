from fastapi import APIRouter
from app.services import statistics_service as ss

router = APIRouter()

@router.get("/statistics/{province_id}")
def get_top_languages(province_id: str):
    return ss.get_top_languages(province_id)