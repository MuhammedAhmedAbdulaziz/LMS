# user_operations.py

from database import get_db_connection
from datetime import datetime, timedelta

def search_available_books(query=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if query:
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT id, title, author, category FROM books 
            WHERE status = 'available' AND (title LIKE %s OR author LIKE %s)
        """, (search_term, search_term))
    else:
        cursor.execute("SELECT id, title, author, category FROM books WHERE status = 'available'")
        
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return books

def borrow_book(user_id, username, book_id, days_to_borrow):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM books WHERE id = %s", (book_id,))
    book_status = cursor.fetchone()

    if book_status and book_status[0] == 'available':
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=days_to_borrow)
        
        borrow_date_str = borrow_date.strftime('%Y-%m-%d %H:%M:%S')
        due_date_str = due_date.strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("UPDATE books SET status = 'borrowed' WHERE id = %s", (book_id,))
        cursor.execute("""
            INSERT INTO transactions (user_id, username, book_id, borrow_date, due_date) 
            VALUES (%s, %s, %s, %s, %s)
            """, (user_id, username, book_id, borrow_date_str, due_date_str))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    cursor.close()
    conn.close()
    return False

def return_book(user_id, book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM transactions
        WHERE user_id = %s AND book_id = %s AND return_date IS NULL
    """, (user_id, book_id))
    transaction = cursor.fetchone()

    if transaction:
        return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE books SET status = 'available' WHERE id = %s", (book_id,))
        cursor.execute("UPDATE transactions SET return_date = %s WHERE id = %s", (return_date, transaction[0]))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    cursor.close()
    conn.close()
    return False

def view_borrowing_history(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.title, t.borrow_date, t.due_date, t.return_date, t.book_id
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        WHERE t.user_id = %s
        ORDER BY t.borrow_date DESC
    """, (user_id,))
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history