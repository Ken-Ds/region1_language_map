# app/routes/phrase_routes.py
from fastapi import APIRouter
from app.models import Phrase
from app.services import phrase_service as ps

router = APIRouter()

@router.get("/phrases", response_model=list[Phrase])
def read_phrases():
    return ps.get_all_phrases()

@router.post("/phrases")
def add_phrase(p: Phrase):
    return ps.create_phrase(p)

@router.put("/phrases/{phrase_id}")
def modify_phrase(phrase_id: str, p: Phrase):
    return ps.update_phrase(phrase_id, p)

@router.delete("/phrases/{phrase_id}")
def remove_phrase(phrase_id: str):
    return ps.delete_phrase(phrase_id)

@router.get("/phrases/comparison/{province_id}")
def get_phrase_comparison(province_id: str):
    return ps.get_phrase_comparison_by_province(province_id)