from setup_db import establish_connection
from loguru import logger
from flask import url_for

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
        (entry[0], entry[1], entry[2], entry[3], entry[4], entry[6][0]['resource'], entry[6][0]['link'], entry[7])]
    logger.info(timeline_entries)

    cursor.executemany(f"""
        INSERT INTO {timeline}_timeline (title, image_url, date_range, description, side, resource, link, tags)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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

def get_search_query(search_query):
    try:
        connection = establish_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("USE devops_journey")
        results = []
        tables = ['aqa_timeline', 'devops_timeline', 'projects']
        column_name = 'description'
        logger.info(f"Getting search query {search_query} from database")
        for table in tables:
            query = f"""
                SELECT * FROM `{table}`
                WHERE `{column_name}` LIKE %s
            """
            cursor.execute(query, (f'%{search_query}%',))
            rows = cursor.fetchall()
            for row in rows:
                match table:
                    case 'aqa_timeline':
                        row['source_url'] = url_for('aqa_timeline')
                        row['source_type'] = 'Timeline'
                    case 'devops_timeline':
                        row['source_url'] = url_for('devops_timeline')
                        row['source_type'] = 'Timeline'
                    case 'projects':
                        row['source_url'] = url_for('projects')
                        row['source_type'] = 'Projects'
            results.extend(rows)
            logger.info(results)
        cursor.close()
        connection.close()
        return results
    except Exception as err:
        logger.info(f"Error: {err}")


def add_activity_entry(description, image_location, activity_date):
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("USE devops_journey")
    table_name = 'activities'
    logger.info(f'Activity data: description: {description}, image location: {image_location}, activity date: {activity_date}')
    cursor.execute(f"""
                INSERT INTO {table_name} (description, image_location, activity_date)
                VALUES (%s, %s, %s)
            """, (description, image_location, activity_date))
    connection.commit()
    activity_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return activity_id

def get_activity_entries():
    try:
        connection = establish_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("USE devops_journey")
        results = []
        table = 'activities'
        logger.info(f"Getting activity entries from database")
        query = f"""
                SELECT * FROM `{table}`
            """
        cursor.execute(query)
        results.extend(cursor.fetchall())
        cursor.close()
        connection.close()
        logger.info(f'List of activities: {results}')
        return results
    except Exception as err:
        logger.info(f"Error: {err}")