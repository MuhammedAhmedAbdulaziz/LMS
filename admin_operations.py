# admin_operations.py

import os
import gzip
import shutil
import sqlite3
import hashlib
from database import get_db_connection
from datetime import datetime

def add_book(title, author, category):
    """Adds a new book to the database."""
    # (No changes to this function)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, category) VALUES (?, ?, ?)", (title, author, category))
    conn.commit()
    conn.close()

def view_all_books():
    """Displays all books in the system."""
    # (No changes to this function)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, category, status FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def get_book_details(book_id):
    """Retrieves the details for a single book by its ID."""
    # (No changes to this function)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, category FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    return book

def update_book_field(book_id, field_to_update, new_value):
    """Updates a single field of a book's details. Returns True on success, False on failure."""
    allowed_fields = ['title', 'author', 'category']
    if field_to_update not in allowed_fields:
        print("Error: Invalid field specified for update.")
        return False

    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"UPDATE books SET {field_to_update} = ? WHERE id = ?"
    cursor.execute(query, (new_value, book_id))
    
    # Check if a row was actually updated. If not, the book_id didn't exist.
    if cursor.rowcount == 0:
        conn.close()
        return False
        
    conn.commit()
    conn.close()
    return True

def delete_book(book_id):
    """Deletes a book from the database. Returns True on success, False on failure."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    
    # Check if a row was actually deleted.
    if cursor.rowcount == 0:
        conn.close()
        return False
        
    conn.commit()
    conn.close()
    return True

def view_all_borrowing_records():
    """Displays all borrowing and returning activities, including due date."""
    # (No changes to this function)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.username, b.title, t.borrow_date, t.due_date, t.return_date
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        ORDER BY t.borrow_date DESC
    """)
    records = cursor.fetchall()
    conn.close()
    return records
    
def create_user(username, password, role):
    """Creates a new user or admin with a hashed password, callable only by an admin."""
    # (No changes to this function)
    if role not in ['user', 'admin']:
        print("Error: Invalid role specified. Must be 'user' or 'admin'.")
        return False
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, password_hash, role))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: This username is already taken.")
        return False
    finally:
        conn.close()
    return True

def disk_usage_alert_system():
    """Scans for large files, compresses them, and logs the event."""
    # (No changes to this function)
    alerts = []
    current_directory = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(current_directory):
        filepath = os.path.join(current_directory, filename)
        if os.path.isfile(filepath):
            file_size_gb = os.path.getsize(filepath) / (1024 * 1024 * 1024)
            if file_size_gb >= 1:
                try:
                    with open(filepath, 'rb') as f_in, gzip.open(f'{filepath}.gz', 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                    os.remove(filepath)
                    log_message = f"Compressed {filename} due to large size ({file_size_gb:.2f} GB)."
                    alerts.append(log_message)
                    log_action("System Alert", log_message)
                except Exception as e:
                    error_message = f"Error compressing {filename}: {e}"
                    alerts.append(error_message)
                    log_action("System Error", error_message)
    return alerts

def log_action(action, details):
    """Logs an action to the logs table."""
    # (No changes to this function)
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO logs (timestamp, action, details) VALUES (?, ?, ?)",
                   (timestamp, action, details))
    conn.commit()
    conn.close()