# auth.py

import sqlite3
import hashlib
from database import get_db_connection

def login(username, password):
    """Authenticates a user by comparing hashed passwords and returns their role."""
    # Hash the password provided by the user to compare it with the stored hash
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return user['role']
    return None

def signup(username, password):
    """Creates a new user with the 'user' role and a hashed password."""
    # Never store plain text passwords! Always hash them.
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    role = 'user'  # Public signups are always for standard users

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, password_hash, role))
        conn.commit()
    except sqlite3.IntegrityError:
        # This error occurs if the username is already taken (due to UNIQUE constraint)
        return False
    finally:
        conn.close()

    return True

def get_user_id(username):
    """Gets the user ID for a given username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id['id'] if user_id else None