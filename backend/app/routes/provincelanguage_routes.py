from fastapi import APIRouter
from app.models import ProvinceLanguage
from app.services import provincelanguage_service as pls

router = APIRouter()

@router.get("/provincelanguages", response_model=list[ProvinceLanguage])
def read_province_languages():
    return pls.get_all_province_languages()

@router.get("/provincelanguages/top10/{province_id}")
def read_top10_dialects_by_province(province_id: str):
    return pls.get_top10_dialects_by_province(province_id)

@router.post("/provincelanguages")
def add_province_language(p: ProvinceLanguage):
    return pls.create_province_language(p)

@router.get("/provincelanguages/statistics/{province_id}")
def get_language_statistics(province_id: str):
    return pls.get_language_statistics_by_province(province_id)