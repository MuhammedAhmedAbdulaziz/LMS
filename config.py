# config.py

import os

# PostgreSQL connection details.
# Using os.getenv allows you to configure the database via environment variables,
# which is essential for containerization (Docker, Kubernetes).
DB_NAME = os.getenv("DB_NAME", "library")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")