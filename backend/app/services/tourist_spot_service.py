from app.db import get_connection
from app.models import Popular
from fastapi import HTTPException

def get_tourist_spots_by_province(province_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT NAME, LOCATION
        FROM popular
        WHERE PROVINCE_ID = %s
          AND TYPE = 'Place'
    """
    cursor.execute(query, (province_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if not results:
        raise HTTPException(status_code=404, detail="No tourist spots found for this province")

    return results
