# auth.py

import psycopg2
import hashlib
from database import get_db_connection

def login(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password_hash))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        return user[0]  # PostgreSQL returns tuples
    return None

def signup(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    role = 'user'

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (username, password_hash, role))
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        return False
    finally:
        cursor.close()
        conn.close()

def get_user_id(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_id[0] if user_id else None