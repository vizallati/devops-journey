import time
import mysql.connector
from loguru import logger



def establish_connection():
    config = {
        'user': 'root',
        'password': 'my-secret-pw',
        'host': 'db'
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

def create_table(timeline):
    table_name = f'{timeline}_timeline'
    logger.info(f'table name is: {table_name}')
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("USE devops_journey")
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            image_url VARCHAR(255),
            date_range VARCHAR(50),
            description TEXT,
            side ENUM('left', 'right'),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()
    logger.info(f"Table: {table_name} successfully created")


if __name__=="__main__":
    logger.info("Waiting 15 seconds for Database to initialize...")
    time.sleep(15)
    create_database()
    create_table(timeline='devops')
    create_table(timeline='aqa')