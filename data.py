from setup_db import establish_connection
from loguru import logger

def get_timeline_data():
    try:
        connection = establish_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("USE devops_journey")
        logger.info("Getting timeline data")
        cursor.execute("SELECT * FROM timeline")
        rows = cursor.fetchall()
        for row in rows:
            logger.info(f"Title: {row['title']}, Date Range: {row['date_range']}, Description: {row['description']}")
        cursor.close()
        connection.close()
        return rows
    except Exception as err:
        logger.info(f"Error: {err}")


def get_recent_timeline_entries(limit=5):
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("USE devops_journey")

        cursor.execute("""
            SELECT * FROM timeline ORDER BY created_at DESC LIMIT %s
        """, (limit,))
        recent_entries = cursor.fetchall()
        return recent_entries
    except Exception as err:
        logger.info(f"Error: {err}")
        return []
    finally:
        cursor.close()
        connection.close()


def add_timeline_entry(entry):
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("USE devops_journey")
    timeline_entries = [
        (entry[0], entry[1], entry[2], entry[3], entry[4])]

    cursor.executemany("""
        INSERT INTO timeline (title, image_url, date_range, description, side)
        VALUES (%s, %s, %s, %s, %s)
    """, timeline_entries)
    connection.commit()
    cursor.close()
    connection.close()
