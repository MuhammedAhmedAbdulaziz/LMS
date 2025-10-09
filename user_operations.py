# user_operations.py

from database import get_db_connection
from datetime import datetime, timedelta

def search_available_books(query=None):
    """
    Searches for available books by title or author.
    If no query is provided, it returns all available books.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if query:
        # Use LIKE for partial matches
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT id, title, author, category FROM books 
            WHERE status = 'available' AND (title LIKE ? OR author LIKE ?)
        """, (search_term, search_term))
    else:
        # If no query, just get all available books
        cursor.execute("SELECT id, title, author, category FROM books WHERE status = 'available'")
        
    books = cursor.fetchall()
    conn.close()
    return books

def borrow_book(user_id, username, book_id, days_to_borrow):
    """Borrows a book for a user for a specified number of days."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM books WHERE id = ?", (book_id,))
    book_status = cursor.fetchone()

    if book_status and book_status['status'] == 'available':
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=days_to_borrow)
        
        borrow_date_str = borrow_date.strftime('%Y-%m-%d %H:%M:%S')
        due_date_str = due_date.strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("UPDATE books SET status = 'borrowed' WHERE id = ?", (book_id,))
        cursor.execute("""
            INSERT INTO transactions (user_id, username, book_id, borrow_date, due_date) 
            VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, book_id, borrow_date_str, due_date_str))
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False

def return_book(user_id, book_id):
    """Returns a borrowed book."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM transactions
        WHERE user_id = ? AND book_id = ? AND return_date IS NULL
    """, (user_id, book_id))
    transaction = cursor.fetchone()

    if transaction:
        return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE books SET status = 'available' WHERE id = ?", (book_id,))
        cursor.execute("UPDATE transactions SET return_date = ? WHERE id = ?", (return_date, transaction['id']))
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False

def view_borrowing_history(user_id):
    """Displays the borrowing history for a user, including the due date."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.title, t.borrow_date, t.due_date, t.return_date, t.book_id
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        WHERE t.user_id = ?
        ORDER BY t.borrow_date DESC
    """, (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history