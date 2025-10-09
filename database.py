# database.py

import sqlite3
import hashlib
from config import DATABASE_NAME

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Creates the necessary tables in the database if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user', 'admin'))
        );
    ''')

    # Create books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            status TEXT NOT NULL DEFAULT 'available' CHECK(status IN ('available', 'borrowed'))
        );
    ''')

    # Create transactions table (UPDATED SCHEMA)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            book_id INTEGER NOT NULL,
            borrow_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (book_id) REFERENCES books (id)
        );
    ''')

    # Create logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT
        );
    ''')

    # Add a default admin if one doesn't exist (with a hashed password)
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_pass_hashed = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ('admin', admin_pass_hashed, 'admin'))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print("Database and tables created successfully.")