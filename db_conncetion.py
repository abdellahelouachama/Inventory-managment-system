import os
import pymysql

def create_connection():
    password = os.environ.get('DB_PASSWORD')
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password=password,
        database="store"
    )
    return  mydb

def get_cursor(connection):
    mycursor = connection.cursor()
    return mycursor

def close_connection(connection, cursor):
    cursor.close()
    connection.close()