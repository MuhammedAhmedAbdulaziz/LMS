# config.py

import os

# Use environment variable for database URL (for production) or local for development
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/library')