# Use an official lightweight Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
# This includes app.py, auth.py, templates/, static/, etc.
COPY . .

# Expose port 5000 to allow communication to the app
EXPOSE 5000

# Command to run the Flask application
# The "--host=0.0.0.0" is crucial to make the server accessible from outside the container
CMD ["flask", "run", "--host=0.0.0.0"]