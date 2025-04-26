# app/routes/language_routes.py
from fastapi import APIRouter
from app.models import Language
from app.services import language_service as ls

router = APIRouter()

@router.get("/languages", response_model=list[Language])
def read_languages():
    return ls.get_languages()

@router.post("/languages")
def add_language(language: Language):
    return ls.create_language(language)

@router.put("/languages/{language_id}")
def modify_language(language_id: str, language: Language):
    return ls.update_language(language_id, language)

@router.delete("/languages/{language_id}")
def remove_language(language_id: str):
    return ls.delete_language(language_id)

@router.get("/languages/municipality/{municipality_id}")
def read_languages_by_municipality(municipality_id: str):
    return ls.get_languages_by_municipality(municipality_id)

@router.get("/languages/province/{province_id}")
def read_languages_by_province(province_id: str):
    return ls.get_languages_by_province(province_id)

@router.get("/languages/municipality/{municipality_id}/top3")
def read_top3_languages_by_municipality(municipality_id: str):
    return ls.get_top3_languages_by_municipality(municipality_id)

@router.get("/languages/province/{province_id}/top10")
def read_top10_languages_by_province(province_id: str):
    return ls.get_top10_languages_by_province(province_id)