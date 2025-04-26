from fastapi import HTTPException
from app.db import get_connection
from app.models import Phrase

def get_all_phrases():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM phrases")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def create_phrase(p: Phrase):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO phrases (PHRASE_ID, CONTENT, LANGUAGE_ID) VALUES (%s, %s, %s)",
                   (p.PHRASE_ID, p.CONTENT, p.LANGUAGE_ID))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Phrase added successfully"}

def update_phrase(phrase_id: str, p: Phrase):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE phrases SET CONTENT = %s, LANGUAGE_ID = %s WHERE PHRASE_ID = %s",
                   (p.CONTENT, p.LANGUAGE_ID, phrase_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Phrase not found")
    cursor.close()
    conn.close()
    return {"message": "Phrase updated successfully"}

def delete_phrase(phrase_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM phrases WHERE PHRASE_ID = %s", (phrase_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Phrase not found")
    cursor.close()
    conn.close()
    return {"message": "Phrase deleted successfully"}

def get_phrase_comparison_by_province(province_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Step 1: Get dialects spoken in the province
    cursor.execute("""
        SELECT d.DIALECT_ID, d.DIALECT_NAME, d.LANGUAGE_ID, l.NAME AS LANGUAGE_NAME
        FROM provincelanguages pl
        JOIN dialects d ON pl.DIALECT_ID = d.DIALECT_ID
        JOIN languages l ON d.LANGUAGE_ID = l.LANGUAGE_ID
        WHERE pl.PROVINCE_ID = %s
    """, (province_id,))
    dialects = cursor.fetchall()

    language_ids = [d['LANGUAGE_ID'] for d in dialects]
    language_map = {d['LANGUAGE_ID']: d['LANGUAGE_NAME'] for d in dialects}

    if not language_ids:
        return []

    # Step 2: Get phrases in those languages
    format_strings = ','.join(['%s'] * len(language_ids))
    cursor.execute(f"""
        SELECT PHRASE_ID, CONTENT, LANGUAGE_ID, ENGLISH_TRANSLATION
        FROM phrases
        WHERE LANGUAGE_ID IN ({format_strings})
    """, tuple(language_ids))
    rows = cursor.fetchall()

    # Step 3: Group by PHRASE_ID
    phrase_map = {}
    for row in rows:
        phrase_id = row['PHRASE_ID']
        lang_name = language_map.get(row['LANGUAGE_ID'], row['LANGUAGE_ID'])
        if phrase_id not in phrase_map:
            phrase_map[phrase_id] = {
                "phrase_id": phrase_id,
                "content": row['CONTENT'],  # Add phrase content
                "english_translation": row['ENGLISH_TRANSLATION'],  # Add English translation
                "translations": {}
            }
        phrase_map[phrase_id]["translations"][lang_name] = row['CONTENT']

    cursor.close()
    conn.close()

    return list(phrase_map.values())