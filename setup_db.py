import mysql.connector
from loguru import logger


def establish_connection():
    config = {
        'user': 'root',
        'password': 'my-secret-pw',
        'host': 'localhost'
    }
    return mysql.connector.connect(**config)

def create_database(db_name='devops_journey'):
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("CREATE DATABASE IF NOT EXISTS devops_journey")
    cursor.execute(f"USE {db_name}")
    connection.commit()
    cursor.close()
    connection.close()
    logger.info(f"Table: {db_name} successfully created!")

def create_table(table_name='timeline'):
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            image_url VARCHAR(255),
            date_range VARCHAR(50),
            description TEXT,
            side ENUM('left', 'right')
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()
    logger.info(f"Table: {table_name} successfully created")


if __name__=="__main__":
    create_database()
    create_table()