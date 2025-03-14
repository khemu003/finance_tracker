import sqlite3

def get_db_connection():
    conn = sqlite3.connect("finance.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enables dictionary-style access
    return conn
