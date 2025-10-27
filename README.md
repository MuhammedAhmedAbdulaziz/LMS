# Library Management System (LMS)

A full-stack Library Management System built with Flask and PostgreSQL, designed to be deployed as a containerized application on Kubernetes. This project serves as a practical example of applying DevOps principles, including containerization, orchestration, and configuration management.


## ✨ Features

The application provides a complete set of features for both library users and administrators.

### User Features
- **Authentication:** Secure user signup and login.
- **Book Search:** Search the library catalog for available books by title or author.
- **Borrow Books:** Borrow available books for a specified number of days.
- **Return Books:** Return currently borrowed books.
- **Borrowing History:** View a complete history of all borrowed and returned books.

### Admin Features
- **Full Book Management (CRUD):**
  - **Add:** Add new books to the library catalog.
  - **Update:** Modify the details (title, author, category) of existing books.
  - **Delete:** Remove books from the system.
- **View All Books:** See a complete list of all books and their current status (available/borrowed).
- **User Management:** Create new user or admin accounts.
- **Transaction Monitoring:** View a global log of all borrowing and return activities across all users.

## 💻 Tech Stack

- **Backend:** Python 3.9, Flask
- **WSGI Server:** Gunicorn
- **Database:** PostgreSQL
- **Containerization:** Docker & Docker Compose (for local development)
- **Orchestration:** Kubernetes (deployment on Minikube)
- **Frontend:** HTML, CSS, Vanilla JavaScript

## 🚀 Getting Started

There are two ways to run this application: locally using Docker Compose for development and testing, or deployed on a Kubernetes cluster (Minikube) for a production-like environment.

### Default Admin Credentials

A default administrator account is created when the database is first initialized. Use these credentials to log in for the first time:

- **Username:** `admin`
- **Password:** `admin123`

### 1. Local Development (with Docker Compose)

This is the recommended method for local development and testing.

**Prerequisites:**
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/) 

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone -b migrate-to-postgres --single-branch https://github.com/MuhammedAhmedAbdulaziz/LMS.git 
    cd LMS
    ```

2.  **Build and run the application:**
    This single command will build the Flask application image, pull the PostgreSQL image, and start both containers in a networked environment.
    ```bash
    docker-compose up --build
    ```

3.  **Access the application:**
    Open your web browser and navigate to **`http://localhost:5000`**. The application should be fully functional.

4.  **Stopping the application:**
    To stop the services, press `CTRL+C` in the terminal. To clean up the containers and the network, run:
    ```bash
    docker-compose down
    ```
    To perform a full cleanup, including the database volume (all data will be lost), run:
    ```bash
    docker-compose down -v
    ```

### 2. Deployment on Kubernetes (with Minikube)

This section guides you through deploying the application to a local Kubernetes cluster.

**Prerequisites:**
- [Docker](https://www.docker.com/get-started)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- A Docker Hub account to push your application image.

**Steps:**

1.  **Build and Push the Docker Image:**
    The Kubernetes cluster needs to pull your application image from a container registry.
    ```bash
    # 1. Log in to your Docker Hub account
    docker login

    # 2. Build and tag your image (replace 'your-dockerhub-username')
    docker build -t your-dockerhub-username/library-app:latest .

    # 3. Push the image to Docker Hub
    docker push your-dockerhub-username/library-app:latest
    ```

2.  **Update the Kubernetes Manifest:**
    Open the file `k8s/04-flask-app-deployment.yml` and change the `image` field to the one you just pushed:
    ```yaml
    # ... inside k8s/04-flask-app-deployment.yml
    spec:
      containers:
        - name: flask-app
          # IMPORTANT: Update this line
          image: your-dockerhub-username/library-app:latest
    ```

3.  **Start Minikube:**
    ```bash
    minikube start
    ```

4.  **Apply the Kubernetes Manifests:**
    This command will create the namespace, secret, database, and application resources in your Minikube cluster.
    ```bash
    kubectl apply -f k8s/
    ```

5.  **Check the Deployment Status:**
    Wait for all pods to be in the `Running` state.
    ```bash
    kubectl get all -n library-app
    ```

6.  **Access the Application:**
    Minikube provides a command to easily get the URL for your service.
    ```bash
    minikube service flask-app-service --url -n library-app
    ```
    This will print a URL. Open this URL in your browser to use the application.

7.  **Cleaning Up:**
    To delete all the resources created on Minikube, simply delete the namespace:
    ```bash
    kubectl delete namespace library-app
    ```

## 📂 Project Structure
```
.
├── k8s/                  # Kubernetes manifest files
├── screenshots/          # Application screenshots
│   ├── admin_dashboard.png
│   └── user_dashboard.png
├── static/               # Static files (CSS)
├── templates/            # HTML templates
├── admin_operations.py   # Data logic for admin functions
├── app.py                # Main Flask application file
├── auth.py               # Authentication logic
├── config.py             # Configuration (DB connection details)
├── database.py           # Database connection and table creation
├── user_operations.py    # Data logic for user functions
├── Dockerfile            # Instructions to build the application image
├── docker-compose.yml    # Defines services for local development
├── requirements.txt      # Python dependencies
└── README.md             
```

## 📈 Future Improvements
- [ ] Implement a CI/CD pipeline using GitHub Actions to automate testing and deployment.
- [ ] Add database migrations using a tool like Alembic.
- [ ] Enhance the frontend with a modern JavaScript framework like React or Vue.js.
- [ ] Add more features like book reservations, fine calculations for overdue books, and user reviews.
