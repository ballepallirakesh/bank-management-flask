import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",              # Change this if your MySQL username is different
        password="12345", # 🔐 Change this to your real MySQL password
        database="bank_db"
    )
