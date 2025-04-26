# app/routes/municipality_routes.py
from fastapi import APIRouter, HTTPException
from app.models import Municipality
from app.services import municipality_service as ms

router = APIRouter()

@router.get("/municipalities", response_model=list[Municipality])
def read_municipalities():
    return ms.get_all_municipalities()

@router.get("/municipalities/province/{province_id}", response_model=list[Municipality])
def read_municipalities_by_province(province_id: str):
    return ms.get_municipalities_by_province(province_id)

@router.post("/municipalities")
def add_municipality(municipality: Municipality):
    return ms.create_municipality(municipality)

@router.put("/municipalities/{municipality_id}")
def modify_municipality(municipality_id: str, municipality: Municipality):
    return ms.update_municipality(municipality_id, municipality)

@router.delete("/municipalities/{municipality_id}")
def remove_municipality(municipality_id: str):
    return ms.delete_municipality(municipality_id)