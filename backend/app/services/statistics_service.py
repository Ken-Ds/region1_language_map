from app.db import get_connection
from fastapi import HTTPException

def get_top_languages(province_id: str):
    try:
        # Connect to the database
        conn = get_connection()
        cursor = conn.cursor()

        # Query to get top 3 languages for each municipality in the province
        query_municipality = """
            SELECT m.NAME AS municipality_name, l.NAME AS language, COUNT(*) AS language_count
            FROM municipalities m
            JOIN municipalitylanguages ml ON m.MUNICIPALITY_ID = ml.MUNICIPALITY_ID
            JOIN languages l ON ml.LANGUAGE_ID = l.LANGUAGE_ID
            WHERE m.PROVINCE_ID = %s
            GROUP BY m.NAME, l.NAME
            ORDER BY m.NAME, language_count DESC;
        """

        cursor.execute(query_municipality, (province_id,))
        municipality_data = cursor.fetchall()

        # Prepare dictionary to hold language stats by municipality
        municipality_stats = {}
        for row in municipality_data:
            municipality_name = row[0]
            language = row[1]
            
            if municipality_name not in municipality_stats:
                municipality_stats[municipality_name] = []

            # Limit to top 3 languages per municipality
            if len(municipality_stats[municipality_name]) < 3:
                municipality_stats[municipality_name].append(language)

        # Query to get overall top 10 languages
        query_overall = """
            SELECT l.NAME AS language, COUNT(*) AS language_count
            FROM municipalitylanguages ml
            JOIN languages l ON ml.LANGUAGE_ID = l.LANGUAGE_ID
            JOIN municipalities m ON ml.MUNICIPALITY_ID = m.MUNICIPALITY_ID
            WHERE m.PROVINCE_ID = %s
            GROUP BY l.NAME
            ORDER BY language_count DESC
            LIMIT 10;
        """

        cursor.execute(query_overall, (province_id,))
        overall_data = cursor.fetchall()

        # Prepare overall top 10 languages list
        overall_stats = [row[0] for row in overall_data]

        # Close database connection
        cursor.close()
        conn.close()

        return {"municipality_stats": municipality_stats, "overall_stats": overall_stats}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")
