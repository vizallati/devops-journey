import os
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
            resource VARCHAR(255) NOT NULL,
            link VARCHAR(255),
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()
    logger.info(f"Table: {table_name} successfully created")


def create_project_table():
    table_name = 'projects'
    logger.info(f'table name is: {table_name}')
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("USE devops_journey")
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            image_location VARCHAR(255),
            description TEXT,
            resource VARCHAR(255) NOT NULL,
            link VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()
    logger.info(f"Table: {table_name} successfully created")


def create_activity_table():
    table_name = 'activities'
    logger.info(f'table name is: {table_name}')
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("USE devops_journey")
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            description VARCHAR(255) NOT NULL,
            image_location VARCHAR(255),
            activity_date DATE,
            likes INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()
    logger.info(f"Table: {table_name} successfully created")

def create_comment_table():
    table_name = 'comments'
    logger.info(f'table name is: {table_name}')
    connection = establish_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("USE devops_journey")
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            activity_id INT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()
    logger.info(f"Table: {table_name} successfully created")



if __name__=="__main__":
    logger.info("Setting up database...")
    create_database()
    create_table(timeline='devops')
    create_table(timeline='aqa')
    create_activity_table()
    create_comment_table()
    create_project_table()