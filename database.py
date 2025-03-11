import sqlite3

def get_db_connection():
    return sqlite3.connect("finance.db", check_same_thread=False)
