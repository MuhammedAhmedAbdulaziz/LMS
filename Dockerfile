# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define environment variables that will be passed in by Docker Compose or Kubernetes
# These are placeholders; the actual values will be set during runtime.
ENV DB_HOST=postgres
ENV DB_NAME=library
ENV DB_USER=user
ENV DB_PASS=password
ENV DB_PORT=5432

# The command to run the application using Gunicorn
# Gunicorn is a production-ready WSGI server.
# We bind to 0.0.0.0 to allow traffic from outside the container.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]