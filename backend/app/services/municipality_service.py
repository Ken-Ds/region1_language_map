from fastapi import HTTPException
from app.db import get_connection
from app.models import Municipality

def get_all_municipalities():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM municipalities")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_municipalities_by_province(province_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM municipalities WHERE PROVINCE_ID = %s", (province_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if not results:
        raise HTTPException(status_code=404, detail="No municipalities found for this province")
    return results

def create_municipality(m: Municipality):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO municipalities (MUNICIPALITY_ID, NAME, INFORMATION, PROVINCE_ID) VALUES (%s, %s, %s, %s)",
                   (m.MUNICIPALITY_ID, m.NAME, m.INFORMATION, m.PROVINCE_ID))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Municipality added successfully"}

def update_municipality(municipality_id: str, m: Municipality):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE municipalities SET NAME = %s, INFORMATION = %s, PROVINCE_ID = %s WHERE MUNICIPALITY_ID = %s",
                   (m.NAME, m.INFORMATION, m.PROVINCE_ID, municipality_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Municipality not found")
    cursor.close()
    conn.close()
    return {"message": "Municipality updated successfully"}

def delete_municipality(municipality_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM municipalities WHERE MUNICIPALITY_ID = %s", (municipality_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Municipality not found")
    cursor.close()
    conn.close()
    return {"message": "Municipality deleted successfully"}