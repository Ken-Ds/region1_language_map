from fastapi import APIRouter
from app.models import Popular
from app.services import delicacy_service as ps

router = APIRouter()

@router.get("/popular/foods/{province_id}")
def read_foods_by_province(province_id: str):
    return ps.get_all_foods_by_province(province_id)
