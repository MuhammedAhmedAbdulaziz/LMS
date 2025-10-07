# **Library Management System - Project Documentation**

This document provides a comprehensive overview of the Library Management System web application, including its architecture, setup instructions, features, and code structure.

### **Table of Contents**
1.  [Project Overview](#1-project-overview)
2.  [Technology Stack](#2-technology-stack)
3.  [Architectural Design](#3-architectural-design)
4.  [Setup and Installation Guide](#4-setup-and-installation-guide)
5.  [Database Schema](#5-database-schema)
6.  [Features and Functionality](#6-features-and-functionality)
7.  [Code Structure and Module Breakdown](#7-code-structure-and-module-breakdown)
8.  [Future Improvements](#8-future-improvements)

---

## **1. Project Overview**

The Library Management System is a full-featured web application built with Python and Flask. It provides a clean, interactive user interface for managing a library's catalog and borrowing activities. The system is designed with two distinct user roles: **Users** and **Admins**, each having access to a specific set of functionalities tailored to their needs.

#### **Core Features:**
*   **Role-Based Access Control:** A secure login system that directs users to their respective dashboards.
*   **User Functionality:** Standard users can sign up, search for available books, borrow books for a specified duration, and view their personal borrowing history.
*   **Admin Functionality:** Administrators have full CRUD (Create, Read, Update, Delete) control over the book catalog. They can also manage user accounts and monitor all transaction records across the system.
*   **Interactive UI:** A modern, responsive web interface that replaces the command-line, providing a seamless user experience.
*   **System Maintenance:** Includes a utility for scanning and compressing large files to manage disk space.

---

## **2. Technology Stack**

*   **Backend:** Python 3, Flask Web Framework
*   **Database:** SQLite 3 (a lightweight, file-based SQL database)
*   **Frontend:** HTML5, CSS3
*   **Standard Python Libraries:** `os`, `sqlite3`, `hashlib`, `datetime`

---

## **3. Architectural Design**

The application is built as a **Monolithic Web Application** using the Flask framework. This architecture keeps all the logic—user authentication, data processing, and UI rendering—within a single, cohesive project structure.

*   **Client-Server Model:** The user's web browser acts as the client. It sends HTTP requests to the Flask server, which then processes these requests, interacts with the SQLite database, and renders HTML templates to send back as a response.
*   **Session-Based Authentication:** The application uses Flask's secure session management to keep track of logged-in users. Once a user logs in, their `user_id`, `username`, and `role` are stored in a session cookie, allowing the application to identify them across different pages and protect routes.
*   **Modular Backend Logic:** The backend code is organized into distinct modules, each with a clear responsibility (e.g., `auth.py` for authentication, `user_operations.py` for user actions), which keeps the code clean and maintainable.
*   **Templating Engine:** Flask's Jinja2 templating engine is used to dynamically generate HTML pages by embedding backend data (like lists of books) directly into the HTML files.

---

## **4. Setup and Installation Guide**

Follow these steps to get the application running on your local machine.

#### **Prerequisites**
*   Python 3.6 or newer
*   `pip` (Python package installer)

#### **Step 1: Get the Code**
Download and unzip all project files into a single directory named `library_system`.

#### **Step 2: Create a `requirements.txt` File**
In the root of your `library_system` directory, create a file named `requirements.txt` and add the following line to it:
```
Flask
```

#### **Step 3: Install Dependencies**
Open your terminal or command prompt, navigate to the project directory, and run the following command to install Flask:
```bash
pip install -r requirements.txt```

#### **Step 4: Initialize the Database**
Before the first run, it's a good practice to create the database. The application will do this automatically, but you can also do it manually by running:
```bash
python database.py
```
This will create a `library.db` file in your project directory with all the necessary tables.

#### **Step 5: Run the Application**
Execute the main Flask application file:
```bash
python app.py
```

#### **Step 6: Access the Web UI**
Open your web browser and navigate to the following address:
**`http://127.0.0.1:5000`**

You should now see the welcome page with the login/signup form.

#### **Default Admin Credentials**
*   **Username:** `admin`
*   **Password:** `admin123`

---

## **5. Database Schema**

The application uses a single SQLite database file (`library.db`) containing four main tables:

1.  **`users`**
    *   `id` (INTEGER, Primary Key): Unique identifier for each user.
    *   `username` (TEXT, Unique): The user's chosen username.
    *   `password` (TEXT): The user's hashed password.
    *   `role` (TEXT): The user's role ('user' or 'admin').

2.  **`books`**
    *   `id` (INTEGER, Primary Key): Unique identifier for each book.
    *   `title` (TEXT): The title of the book.
    *   `author` (TEXT): The author of the book.
    *   `category` (TEXT): The genre or category.
    *   `status` (TEXT): The current availability ('available' or 'borrowed').

3.  **`transactions`**
    *   `id` (INTEGER, Primary Key): Unique identifier for each transaction.
    *   `user_id` (INTEGER): Foreign key referencing the user who borrowed the book.
    *   `username` (TEXT): The username of the borrowing user.
    *   `book_id` (INTEGER): Foreign key referencing the book that was borrowed.
    *   `borrow_date` (TEXT): The timestamp when the book was borrowed.
    *   `due_date` (TEXT): The calculated timestamp when the book is due.
    *   `return_date` (TEXT): The timestamp when the book was returned (NULL if not yet returned).

4.  **`logs`**
    *   `id` (INTEGER, Primary Key): Unique identifier for each log entry.
    *   `timestamp` (TEXT): The timestamp of the logged event.
    *   `action` (TEXT): The type of action (e.g., 'System Alert').
    *   `details` (TEXT): A description of the event.

---

## **6. Features and Functionality**

#### **For Standard Users:**
*   **Signup:** Create a new user account from the welcome page.
*   **Login/Logout:** Securely log in and out of the system.
*   **Search Books:** Search the catalog for available books by title or author.
*   **Borrow Books:** Select an available book and borrow it for a specified number of days.
*   **Return Books:** Return a book that they have currently borrowed.
*   **View History:** See a personal list of all past and current loans, including due dates.

#### **For Administrators:**
*   **All User Features:** Admins can do everything a standard user can.
*   **Add Books:** Add new books to the library catalog.
*   **Update Books:** Modify the details (title, author, category) of any existing book.
*   **Delete Books:** Permanently remove a book from the catalog.
*   **View All Books:** See a complete list of all books in the system, including their current status.
*   **Create Users:** Create new user or admin accounts directly.
*   **View All Transactions:** Monitor a comprehensive log of all borrowing activities by all users.

---

## **7. Code Structure and Module Breakdown**

*   **`app.py`:** The heart of the Flask application. It defines all the URL routes, handles web requests, processes form data, and renders the HTML templates.
*   **`database.py`:** Responsible for all database interactions: establishing a connection and creating the initial tables and default admin user.
*   **`auth.py`:** Contains all logic related to user authentication, including the `login` and `signup` functions and password hashing.
*   **`user_operations.py`:** Contains all the backend logic for actions that a standard user can perform, such as searching, borrowing, and returning books.
*   **`admin_operations.py`:** Contains all the backend logic for admin-specific actions, like CRUD operations on books and user management.
*   **`config.py`:** A simple configuration file that stores constants, such as the database name.
*   **`templates/` (directory):** Contains all the HTML files that are rendered to the user.
    *   `layout.html`: The master template with the common structure (navbar, footer).
    *   `welcome.html`: The login and signup page.
    *   `user_dashboard.html`: The dashboard for standard users.
    *   `admin_dashboard.html`: The dashboard for administrators.
*   **`static/` (directory):** Contains all static assets.
    *   `css/style.css`: The stylesheet that defines the look and feel of the web application.

---

## **8. Future Improvements**

*   **Microservices Architecture:** To improve scalability and resilience, the application could be broken down into independent microservices (e.g., Auth Service, Catalog Service) that communicate via APIs.
*   **API Token Authentication (JWT):** Replace the session-based login with JSON Web Tokens for a more stateless and secure authentication method, especially if a separate frontend framework is used.
*   **Containerization:** The application can be containerized using **Docker** and orchestrated with **Kubernetes** for easy, scalable, and reliable deployment.
*   **Advanced Features:**
    *   Implement an automatic fining system for overdue books.
    *   Add a book reservation system for books that are currently borrowed.
    *   Include more detailed search filters (e.g., by category, publication year).