import mysql.connector
import pandas as pd
from database import get_db_connection

# User Authentication Functions
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False  # Username already exists
    finally:
        cursor.close()
        conn.close()

def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user[0] if user else None

def fetch_transactions(user_id):
    conn = get_db_connection()
    query = "SELECT * FROM transactions WHERE user_id = %s"
    df = pd.read_sql(query, conn, params=(user_id,))
    conn.close()
    return df

def add_transaction(user_id, date, category, amount, txn_type, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO transactions (user_id, date, category, amount, type, description) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (user_id, date, category, amount, txn_type, description))
    conn.commit()
    cursor.close()
    conn.close()

def delete_transaction(user_id, transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM transactions WHERE id = %s AND user_id = %s"
    cursor.execute(query, (transaction_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def change_transaction(user_id, date, category, amount, txn_type, description, transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE transactions SET date = %s, category = %s, amount = %s, type = %s, description = %s WHERE id = %s AND user_id = %s"
    cursor.execute(query, (date, category, amount, txn_type, description, transaction_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
