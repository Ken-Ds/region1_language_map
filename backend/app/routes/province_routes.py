# app/routes/province_routes.py
from fastapi import APIRouter
from app.models import Province
from app.services import province_service as ps

router = APIRouter()

@router.get("/provinces", response_model=list[Province])
def read_provinces():
    return ps.get_all_provinces()

@router.post("/provinces")
def add_province(province: Province):
    return ps.create_province(province)

@router.put("/provinces/{province_id}")
def modify_province(province_id: str, province: Province):
    return ps.update_province(province_id, province)

@router.delete("/provinces/{province_id}")
def remove_province(province_id: str):
    return ps.delete_province(province_id)