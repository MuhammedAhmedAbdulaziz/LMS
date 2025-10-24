from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import database
import auth
import user_operations as user_ops
import admin_operations as admin_ops
import time

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_for_dev'

# --- DECORATORS ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "danger")
            return redirect(url_for('welcome'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "danger")
            return redirect(url_for('welcome'))
        if session.get('role') != 'admin':
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for('user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# --- AUTHENTICATION ROUTES ---
@app.route("/")
def welcome():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    return render_template("welcome.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    role = auth.login(username, password)
    if role:
        user_id = auth.get_user_id(username)
        session['user_id'] = user_id
        session['username'] = username
        session['role'] = role
        flash(f"Welcome back, {username}!", "success")
        if role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    else:
        flash("Invalid credentials. Please try again.", "danger")
        return redirect(url_for('welcome'))

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    if auth.signup(username, password):
        flash("Account created successfully! Please log in.", "success")
    else:
        flash("Username already exists. Please choose another.", "danger")
    return redirect(url_for('welcome'))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('welcome'))

# --- USER DASHBOARD ROUTE (UPDATED FOR SEARCH) ---
@app.route("/dashboard")
@login_required
def user_dashboard():
    search_query = request.args.get('search', None)
    show_all = request.args.get('show_all', 'false')
    
    available_books = []
    if search_query:
        available_books = user_ops.search_available_books(search_query)
    elif show_all == 'true':
        available_books = user_ops.search_available_books() # No query fetches all

    borrowing_history = user_ops.view_borrowing_history(session['user_id'])
    return render_template("user_dashboard.html",
                           available_books=available_books,
                           history=borrowing_history,
                           search_query=search_query) # Pass query back to template

# --- ADMIN DASHBOARD ROUTE ---
@app.route("/admin")
@admin_required
def admin_dashboard():
    all_books = admin_ops.view_all_books()
    all_transactions = admin_ops.view_all_borrowing_records()
    return render_template("admin_dashboard.html",
                           all_books=all_books,
                           transactions=all_transactions)

# --- ACTION ROUTES (Processing Forms) ---

@app.route("/borrow", methods=["POST"])
@login_required
def borrow():
    # (No changes to this function)
    book_id = request.form.get("book_id")
    days_str = request.form.get("days_to_borrow")
    try:
        days = int(days_str)
        if user_ops.borrow_book(session['user_id'], session['username'], book_id, days):
            flash("Book borrowed successfully!", "success")
        else:
            flash("Failed to borrow book. It may be unavailable.", "danger")
    except (ValueError, TypeError):
        flash("Invalid number of days.", "danger")
    return redirect(url_for('user_dashboard'))

@app.route("/return", methods=["POST"])
@login_required
def return_book():
    book_id = request.form.get("book_id")
    if user_ops.return_book(session['user_id'], book_id):
        flash("Book returned successfully!", "success")
    else:
        flash("Failed to return book. Check if the ID is correct.", "danger")
    return redirect(url_for('user_dashboard'))

@app.route("/add_book", methods=["POST"])
@admin_required
def add_book():
    title = request.form.get("title")
    author = request.form.get("author")
    category = request.form.get("category")
    admin_ops.add_book(title, author, category)
    flash("New book added successfully!", "success")
    return redirect(url_for('admin_dashboard'))

@app.route("/update_book", methods=["POST"])
@admin_required
def update_book():
    book_id = request.form.get("book_id")
    field = request.form.get("field")
    new_value = request.form.get("new_value")
    # UPDATED to handle failure
    if admin_ops.update_book_field(book_id, field, new_value):
         flash(f"Book ID {book_id} was updated successfully!", "success")
    else:
         flash(f"Update failed. Book with ID {book_id} not found.", "danger")
    return redirect(url_for('admin_dashboard'))

@app.route("/delete_book", methods=["POST"])
@admin_required
def delete_book():
    book_id = request.form.get("book_id")
    # UPDATED to handle failure
    if admin_ops.delete_book(book_id):
        flash(f"Book ID {book_id} has been deleted.", "success")
    else:
        flash(f"Delete failed. Book with ID {book_id} not found.", "danger")
    return redirect(url_for('admin_dashboard'))
    
@app.route("/create_user", methods=["POST"])
@admin_required
def create_user():
    # (No changes to this function)
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")
    if admin_ops.create_user(username, password, role):
        flash(f"Account for {username} created successfully.", "success")
    else:
        flash("Failed to create account. Username may be taken.", "danger")
    return redirect(url_for('admin_dashboard'))

if __name__ == "__main__":
    # Give PostgreSQL time to start

    print("⏳ Waiting for database connection...")
    time.sleep(10)
    
    # Create tables
    print("🗃️ Creating database tables...")
    database.create_tables()
    
    print("🚀 Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000)