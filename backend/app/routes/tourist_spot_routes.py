from fastapi import APIRouter
from app.models import Popular
from app.services import tourist_spot_service as ps

router = APIRouter()

@router.get("/popular/tourist-spots/{province_id}")
def read_tourist_spots_by_province(province_id: str):
    return ps.get_tourist_spots_by_province(province_id)