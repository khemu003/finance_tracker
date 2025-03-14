import sqlite3
import pandas as pd
from database import get_db_connection

# User Authentication Functions
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None  # Returns user ID or None

def fetch_transactions(user_id):
    conn = get_db_connection()
    query = "SELECT * FROM transactions WHERE user_id = ?"
    df = pd.read_sql(query, conn, params=(user_id,))
    conn.close()
    return df


def add_transaction(user_id, date, category, amount, txn_type, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO transactions (user_id, date, category, amount, type, description) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (user_id, date, category, amount, txn_type, description))
    conn.commit()
    conn.close()


def delete_transaction(user_id, transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM transactions WHERE id = ? AND user_id = ?"
    cursor.execute(query, (transaction_id, user_id))
    conn.commit()
    conn.close()

def change_transaction(user_id, date, category, amount, txn_type, description, transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE transactions 
    SET date = ?, category = ?, amount = ?, type = ?, description = ? 
    WHERE id = ? AND user_id = ?
    """
    cursor.execute(query, (date, category, amount, txn_type, description, transaction_id, user_id))
    conn.commit()
    conn.close()

