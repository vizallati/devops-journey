from setup_db import establish_connection
from loguru import logger

def get_timeline_data(timeline):
    try:
        connection = establish_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("USE devops_journey")
        logger.info(f"Getting {timeline}_timeline data")
        cursor.execute(f"SELECT * FROM {timeline}_timeline")
        rows = cursor.fetchall()
        for row in rows:
            logger.info(f"Title: {row['title']}, Date Range: {row['date_range']}, Description: {row['description']}")
        cursor.close()
        connection.close()
        return rows
    except Exception as err:
        logger.info(f"Error: {err}")


def get_recent_timeline_entries(timeline, limit=5):
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("USE devops_journey")
        logger.info(f"Getting recent entries from {timeline}_timeline")
        cursor.execute(f"""
            SELECT * FROM {timeline}_timeline ORDER BY created_at DESC LIMIT %s
        """, (limit,))
        recent_entries = cursor.fetchall()
        return recent_entries
    except Exception as err:
        logger.info(f"Error: {err}")
        return []
    finally:
        cursor.close()
        connection.close()


def add_timeline_entry(entry, timeline):
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("USE devops_journey")
    timeline_entries = [
        (entry[0], entry[1], entry[2], entry[3], entry[4], entry[6][0]['resource'], entry[6][0]['link'])]
    logger.info(timeline_entries)

    cursor.executemany(f"""
        INSERT INTO {timeline}_timeline (title, image_url, date_range, description, side, resource, link)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, timeline_entries)
    connection.commit()
    cursor.close()
    connection.close()


def add_project_entry(file_path, entry):
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("USE devops_journey")
    table = 'projects'
    timeline_entries = [
        (entry['title'], file_path, entry['description'], entry['resource'], entry['link'])]
    logger.info(timeline_entries)

    cursor.executemany(f"""
        INSERT INTO {table} (title, image_location, description, resource, link)
        VALUES (%s, %s, %s, %s, %s)
    """, timeline_entries)
    connection.commit()
    cursor.close()
    connection.close()

def get_projects():
    try:
        connection = establish_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("USE devops_journey")
        table = 'projects'
        logger.info(f"Getting {table} data")
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        for row in rows:
            logger.info(f"Title: {row['title']}, Image location: {row['image_location']}, Description: {row['description']}")
        cursor.close()
        connection.close()
        return rows
    except Exception as err:
        logger.info(f"Error: {err}")