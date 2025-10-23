# admin_operations.py

from database import get_db_connection

def add_book(title, author, category):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, category) VALUES (%s, %s, %s)", (title, author, category))
    conn.commit()
    cursor.close()
    conn.close()

def view_all_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, category, status FROM books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return books

def update_book_field(book_id, field_to_update, new_value):
    allowed_fields = ['title', 'author', 'category']
    if field_to_update not in allowed_fields:
        return False

    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"UPDATE books SET {field_to_update} = %s WHERE id = %s"
    cursor.execute(query, (new_value, book_id))
    
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return False
        
    conn.commit()
    cursor.close()
    conn.close()
    return True

def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return False
        
    conn.commit()
    cursor.close()
    conn.close()
    return True

def view_all_borrowing_records():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.username, b.title, t.borrow_date, t.due_date, t.return_date
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        ORDER BY t.borrow_date DESC
    """)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records
    
def create_user(username, password, role):
    if role not in ['user', 'admin']:
        return False
        
    import hashlib
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (username, password_hash, role))
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()