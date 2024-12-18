from setup_db import establish_connection

def get_timeline_data():
    try:
        connection = establish_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("USE devops_journey")
        cursor.execute("SELECT * FROM timeline")
        rows = cursor.fetchall()
        for row in rows:
            print(f"Title: {row['title']}, Date Range: {row['date_range']}, Description: {row['description']}")
        cursor.close()
        connection.close()
        print("Connection closed")
        return rows
    except Exception as err:
        print(f"Error: {err}")
