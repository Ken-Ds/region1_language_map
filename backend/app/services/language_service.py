# app/services/language_service.py
from fastapi import HTTPException
from app.models import Language
from app.db import get_connection

def get_all_languages():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM languages")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_languages_by_municipality(municipality_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT DISTINCT l.*
        FROM languages l
        JOIN municipalitylanguages ml ON l.LANGUAGE_ID = ml.LANGUAGE_ID
        WHERE ml.MUNICIPALITY_ID = %s
    """
    cursor.execute(query, (municipality_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if not results:
        raise HTTPException(status_code=404, detail="No languages found for this municipality")
    return results

def get_top3_languages_by_municipality(municipality_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT l.*, COUNT(*) as language_count
        FROM languages l
        JOIN municipalitylanguages ml ON l.LANGUAGE_ID = ml.LANGUAGE_ID
        WHERE ml.MUNICIPALITY_ID = %s
        GROUP BY l.LANGUAGE_ID
        ORDER BY language_count DESC
        LIMIT 3
    """
    cursor.execute(query, (municipality_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if not results:
        raise HTTPException(status_code=404, detail="No languages found for this municipality")
    return results

def create_language(language: Language):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO languages (LANGUAGE_ID, NAME) VALUES (%s, %s)",
                   (language.LANGUAGE_ID, language.NAME))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Language added successfully"}

def update_language(language_id: str, language: Language):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE languages SET NAME = %s WHERE LANGUAGE_ID = %s",
                   (language.NAME, language_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Language not found")
    cursor.close()
    conn.close()
    return {"message": "Language updated successfully"}

def delete_language(language_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM languages WHERE LANGUAGE_ID = %s", (language_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Language not found")
    cursor.close()
    conn.close()
    return {"message": "Language deleted successfully"}