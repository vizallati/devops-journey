import mysql.connector


def establish_connection():
    config = {
        'user': 'root',
        'password': 'my-secret-pw',
        'host': 'localhost'
    }
    connection = mysql.connector.connect(**config)
    return connection

connection  = establish_connection()
cursor = connection.cursor(dictionary=True)

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS devops_journey")
cursor.execute("USE devops_journey")

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS timeline (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        image_url VARCHAR(255),
        date_range VARCHAR(50),
        description TEXT,
        side ENUM('left', 'right')
    )
""")

# Insert sample data
timeline_entries = [
    ('Docker', 'https://img.icons8.com/?size=100&id=39292&format=png&color=000000', '2018 - 2019', 'Learned about Docker. Stuff like what is Docker, why Docker', 'left'),
    ('Linux System Administration', 'https://img.icons8.com/?size=100&id=17842&format=png&color=000000', '2018 - 2019', 'Learned about Linux System Administration. Stuff like managing servers, configurations', 'right')
]

cursor.executemany("""
    INSERT INTO timeline (title, image_url, date_range, description, side)
    VALUES (%s, %s, %s, %s, %s)
""", timeline_entries)

# Commit the transaction
connection.commit()

# Close the connection
cursor.close()
connection.close()

print("Database and table setup complete with sample data inserted.")
