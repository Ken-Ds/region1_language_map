from app.db import get_connection
from app.models import Popular
from fastapi import HTTPException

def get_all_foods_by_province(province_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT NAME
        FROM popular
        WHERE TYPE = 'Food' AND PROVINCE_ID = %s
    """
    cursor.execute(query, (province_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if not results:
        raise HTTPException(status_code=404, detail="No foods found for this province")

    return results

