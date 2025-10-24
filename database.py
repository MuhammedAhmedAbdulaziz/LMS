import psycopg2
import hashlib
import os
from config import DATABASE_URL

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def create_tables():
    """Creates the necessary tables in the database if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL CHECK(role IN ('user', 'admin'))
        );
    ''')

    # Create books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            category VARCHAR(100),
            status VARCHAR(20) NOT NULL DEFAULT 'available' CHECK(status IN ('available', 'borrowed'))
        );
    ''')

    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            username VARCHAR(255) NOT NULL,
            book_id INTEGER NOT NULL REFERENCES books(id),
            borrow_date TIMESTAMP NOT NULL,
            due_date TIMESTAMP NOT NULL,
            return_date TIMESTAMP
        );
    ''')

    # Add a default admin if one doesn't exist
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_pass_hashed = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       ('admin', admin_pass_hashed, 'admin'))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print("Database and tables created successfully.")