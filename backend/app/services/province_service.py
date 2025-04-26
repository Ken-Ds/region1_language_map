from fastapi import HTTPException
from app.db import get_connection
from app.models import Province

def get_all_provinces():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM provinces")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def create_province(p: Province):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO provinces (PROVINCE_ID, NAME, INFORMATION) VALUES (%s, %s, %s)",
                   (p.PROVINCE_ID, p.NAME, p.INFORMATION))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Province added successfully"}

def update_province(province_id: str, p: Province):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE provinces SET NAME = %s, INFORMATION = %s WHERE PROVINCE_ID = %s",
                   (p.NAME, p.INFORMATION, province_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Province not found")
    cursor.close()
    conn.close()
    return {"message": "Province updated successfully"}

def delete_province(province_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM provinces WHERE PROVINCE_ID = %s", (province_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Province not found")
    cursor.close()
    conn.close()
    return {"message": "Province deleted successfully"}