from fastapi import FastAPI, HTTPException
import pymysql
import os

# Initialize FastAPI
app = FastAPI()

# Database connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""  # blank password for localhost
DB_NAME = "oyly"  # replace with your database name

# Function to get a database connection
def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor  # returns rows as dictionaries
    )
    return connection

# Route to retrieve all records from the `users` table
@app.get("/users")
def read_users():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM contact_us"
            cursor.execute(sql)
            result = cursor.fetchall()  # fetch all rows as a list of dictionaries
    finally:
        connection.close()
    return result
