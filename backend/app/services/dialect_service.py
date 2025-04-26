from fastapi import HTTPException
from app.db import get_connection
from app.models import Dialect

def get_all_dialects():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dialects")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_dialects_by_municipality(municipality_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT d.*
        FROM dialects d
        JOIN municipalitylanguages ml ON d.DIALECT_ID = ml.DIALECT_ID
        WHERE ml.MUNICIPALITY_ID = %s
    """
    cursor.execute(query, (municipality_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if not results:
        raise HTTPException(status_code=404, detail="No dialects found for this municipality")
    return results

def get_dialects_by_province(province_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT d.*
        FROM dialects d
        JOIN provincelanguages pl ON d.DIALECT_ID = pl.DIALECT_ID
        WHERE pl.PROVINCE_ID = %s
    """
    cursor.execute(query, (province_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if not results:
        raise HTTPException(status_code=404, detail="No dialects found for this province")
    return results

def get_top3_dialects_by_municipality(municipality_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT d.*, COUNT(*) as dialect_count
        FROM dialects d
        JOIN municipalitylanguages ml ON d.DIALECT_ID = ml.DIALECT_ID
        WHERE ml.MUNICIPALITY_ID = %s
        GROUP BY d.DIALECT_ID
        ORDER BY dialect_count DESC
        LIMIT 3
    """
    cursor.execute(query, (municipality_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if not results:
        raise HTTPException(status_code=404, detail="No dialects found for this municipality")
    return results

def get_top10_dialects_by_province(province_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT d.*, pl.PERCENTAGE
        FROM dialects d
        JOIN provincelanguages pl ON d.DIALECT_ID = pl.DIALECT_ID
        WHERE pl.PROVINCE_ID = %s
        ORDER BY pl.PERCENTAGE DESC
        LIMIT 10
    """
    cursor.execute(query, (province_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if not results:
        raise HTTPException(status_code=404, detail="No dialects found for this province")
    return results

def create_dialect(d: Dialect):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dialects (DIALECT_ID, DIALECT_NAME, LANGUAGE_ID) VALUES (%s, %s, %s)",
                   (d.DIALECT_ID, d.DIALECT_NAME, d.LANGUAGE_ID))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Dialect added successfully"}

def update_dialect(dialect_id: str, d: Dialect):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE dialects SET DIALECT_NAME = %s, LANGUAGE_ID = %s WHERE DIALECT_ID = %s",
                   (d.DIALECT_NAME, d.LANGUAGE_ID, dialect_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Dialect not found")
    cursor.close()
    conn.close()
    return {"message": "Dialect updated successfully"}

def delete_dialect(dialect_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dialects WHERE DIALECT_ID = %s", (dialect_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Dialect not found")
    cursor.close()
    conn.close()
    return {"message": "Dialect deleted successfully"}