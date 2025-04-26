from fastapi import APIRouter
from app.models import MunicipalityLanguage
from app.services import municipalitylanguage_service as mls

router = APIRouter()

@router.get("/municipalitylanguages", response_model=list[MunicipalityLanguage])
def read_municipality_languages():
    return mls.get_all_municipality_languages()

@router.get("/municipalitylanguages/top3/{municipality_id}")
def read_top3_dialects_by_municipality(municipality_id: str):
    return mls.get_top3_dialects_by_municipality(municipality_id)

@router.post("/municipalitylanguages")
def add_municipality_language(m: MunicipalityLanguage):
    return mls.create_municipality_language(m)