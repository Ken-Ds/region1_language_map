from fastapi import HTTPException
from app.db import get_connection
from app.models import ProvinceLanguage

def get_all_province_languages():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM provincelanguages")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_top10_dialects_by_province(province_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT d.DIALECT_ID, d.DIALECT_NAME, pl.PERCENTAGE
        FROM provincelanguages pl
        JOIN dialects d ON pl.DIALECT_ID = d.DIALECT_ID
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
    
    # Add a percent sign to the PERCENTAGE field with two decimal points
    for result in results:
        result['PERCENTAGE'] = f"{result['PERCENTAGE']:.2f}%"

    return results

def create_province_language(p: ProvinceLanguage):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO provincelanguages (PROVINCE_ID, DIALECT_ID, PERCENTAGE) VALUES (%s, %s, %s)",
                   (p.PROVINCE_ID, p.DIALECT_ID, p.PERCENTAGE))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "ProvinceLanguage added successfully"}

def get_language_statistics_by_province(province_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Query to get the total percentage of speakers for each language in the province
    cursor.execute("""
        SELECT l.NAME AS Language, SUM(pl.PERCENTAGE) AS Percentage
        FROM provincelanguages pl
        JOIN dialects d ON pl.DIALECT_ID = d.DIALECT_ID
        JOIN languages l ON d.LANGUAGE_ID = l.LANGUAGE_ID
        WHERE pl.PROVINCE_ID = %s
        GROUP BY l.NAME
        ORDER BY Percentage DESC
    """, (province_id,))
    language_data = cursor.fetchall()

    # Format the percentage as a string with two decimal places (no extra multiplication)
    for row in language_data:
        row['Percentage'] = f"{row['Percentage']:.2f}%"  # Keep the percentage as-is

    cursor.close()
    conn.close()

    return language_data