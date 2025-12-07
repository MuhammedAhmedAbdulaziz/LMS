# auth.py

import psycopg2
import hashlib
from database import get_db_connection

def login(username, password):
    """Authenticates a user by comparing hashed passwords and returns their role."""
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password_hash))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        return user['role']
    return None

def signup(username, password):
    """Creates a new user with the 'user' role and a hashed password."""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    role = 'user'

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (username, password_hash, role))
        conn.commit()
    except psycopg2.IntegrityError:
        # This error occurs if the username is already taken (due to UNIQUE constraint)
        conn.rollback() # Rollback the failed transaction
        return False
    finally:
        cursor.close()
        conn.close()

    return True

def get_user_id(username):
    """Gets the user ID for a given username."""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_id['id'] if user_id else None