import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv
import os

load_dotenv()

# create mysql connection
def create_connection():
    connection = None

    try:
        connection = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST'),
            port=os.environ.get('MYSQL_PORT'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            db=os.environ.get('MYSQL_DATABASE'),
        )
        print("mysql connection created successfully")
    except Error as e:
        print(f"mysql connection error occured: {e}")

    return connection

# execute mysql query
def execute_query(connection, query):
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()

        return cursor
    except Error as e:
        print(f"mysql query error occured: {e}")

# execute mysql select query
def select_query(connection, query):
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()

        return cursor.fetchall()
    except Error as e:
        print(f"mysql query error occured: {e}")

# close connection
def close_connection(connection):
    if connection:
        connection.close()
        print("mysql connection closed successfully")