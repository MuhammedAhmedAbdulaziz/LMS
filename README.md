# Library Management System - Web Application

![Library System Welcome Page](https://i.imgur.com/eBfJ94c.png)

A full-featured, role-based web application for managing a library's book catalog and borrowing activities. Built with Python and the Flask web framework, this project provides a clean, interactive user interface for both standard users and administrators.

---

### **Table of Contents**
1.  [Project Overview](#project-overview)
2.  [Technology Stack](#technology-stack)
3.  [Live Demo (Screenshots)](#live-demo-screenshots)
4.  [Features and Functionality](#features-and-functionality)
5.  [Setup and Installation Guide](#setup-and-installation-guide)
6.  [Database Schema](#database-schema)
7.  [Code Structure](#code-structure)
8.  [Future Improvements](#future-improvements)

---

## **Project Overview**

The Library Management System is designed to replace traditional command-line interfaces with a modern, responsive web UI. The system provides two distinct user roles, **Users** and **Admins**, each having access to a specific set of functionalities tailored to their needs. The core of the application is a secure, session-based authentication system that ensures data privacy and role-appropriate access.

---

## **Technology Stack**

*   **Backend:** Python 3, Flask Web Framework
*   **Database:** SQLite 3
*   **Frontend:** HTML5, CSS3, Jinja2 Templating
*   **Standard Python Libraries:** `os`, `sqlite3`, `hashlib`, `datetime`

---

## **Live Demo (Screenshots)**

#### **1. Modern Welcome Page**
A single, switchable form for both user Login and Sign Up.
![Welcome Page](https://i.imgur.com/eBfJ94c.png)

#### **2. User Dashboard**
Features a powerful book search, a list of available books, and personal borrowing history.
![User Dashboard](https://i.imgur.com/gK9t0u1.png)

#### **3. Admin Dashboard**
A comprehensive panel for full control over the book catalog, user accounts, and all system transactions.
![Admin Dashboard](https://i.imgur.com/E8w9t8F.png)

---

## **Features and Functionality**

### **For Standard Users (User Role)**
*   **Modern Authentication:** A single, clean interface for both signing up and logging in.
*   **Interactive Book Search:** A dynamic search bar to find available books by title or author, with an option to view all available books.
*   **Book Borrowing:** Borrow any available book for a user-specified number of days.
*   **Book Returning:** Easily return a currently borrowed book with a single click.
*   **Personal History:** View a detailed history of all borrowed books, including borrow dates, due dates, and return status.

### **For Administrators (Admin Role)**
*   **Includes All User Features.**
*   **Full Book Management (CRUD):**
    *   **Create:** Add new books to the library catalog.
    *   **Read:** View a complete list of all books, including their availability status.
    *   **Update:** Selectively update a book's title, author, or category.
    *   **Delete:** Permanently remove a book from the system.
*   **Robust Error Handling:** The system provides clear feedback if an admin tries to update or delete a book with a non-existent ID.
*   **User Account Management:** Create new user or admin accounts directly from the dashboard.
*   **System-Wide Monitoring:** View a comprehensive log of all borrowing transactions across all users.

---

## **Setup and Installation Guide**

Follow these steps to get the application running on your local machine.

#### **1. Prerequisites**
*   Python 3.6 or newer
*   `pip` (Python package installer)

#### **2. Clone the Repository**
```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

#### **3. Install Dependencies**
This project uses Flask. Install it using the following command:
```bash
pip install Flask
```

#### **4. Initialize the Database**
Before running the application for the first time, you must initialize the database. This will create the `library.db` file and all necessary tables.

**Important:** If you are updating the code and encounter a database error, the easiest fix is to delete the old `library.db` file and re-run this step.
```bash
python database.py
```

#### **5. Run the Application**
Execute the main Flask application file:
```bash
python app.py
```

#### **6. Access the Web UI**
Open your web browser and navigate to: **`http://127.0.0.1:5000`**

#### **Default Admin Credentials**
*   **Username:** `admin`
*   **Password:** `admin123`

---

## **Database Schema**

The application uses a single SQLite database file (`library.db`) containing four main tables:

1.  **`users`**: Stores user credentials and roles.
    *   `(id, username, password, role)`
2.  **`books`**: The main catalog of all books.
    *   `(id, title, author, category, status)`
3.  **`transactions`**: A log of all borrowing activities.
    *   `(id, user_id, username, book_id, borrow_date, due_date, return_date)`
4.  **`logs`**: A table for system-level events.
    *   `(id, timestamp, action, details)`

---

## **Code Structure**

*   **`app.py`**: The main Flask application. It handles all web routes, renders HTML, and connects the backend logic to the UI.
*   **`database.py`**: Handles database connection and initial table creation.
*   **`auth.py`**: Manages all authentication logic (login, signup, password hashing).
*   **`user_operations.py`**: Contains the backend logic for all standard user actions (searching, borrowing, returning).
*   **`admin_operations.py`**: Contains the backend logic for all admin-specific actions (book CRUD, user creation).
*   **`templates/`**: Directory containing all HTML files for the user interface.
*   **`static/`**: Directory containing all static assets, such as the `style.css` file.

---

## **Future Improvements**

*   **API-Driven Architecture:** The next logical step is to decouple the backend from the frontend. This involves transforming the backend into a REST API that returns JSON data, allowing for any frontend (web, mobile app) to connect to it.
*   **Containerization:** The application can be containerized using **Docker** and orchestrated with **Kubernetes** to create a scalable, reliable, and easily deployable system.
*   **Advanced Features:**
    *   Implement an automated notification system for overdue books.
    *   Add a book reservation system for books that are currently borrowed.
    *   Include more detailed search filters (e.g., by category, publication year).
```
