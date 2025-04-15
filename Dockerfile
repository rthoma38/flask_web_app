# Use the official Python image
FROM python:3.12-slim

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser

# Set the working directory in the container
WORKDIR /usr/src/app

# Switch to the new user
USER appuser

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /usr/src/app

# Set environment variables securely
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose necessary ports
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
