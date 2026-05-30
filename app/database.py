import os
import mysql.connector


def get_database_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "cinevault"),
        password=os.getenv("DB_PASSWORD", "cinevault123"),
        database=os.getenv("DB_NAME", "cinevault"),
        autocommit=False,
    )
