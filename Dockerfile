# Use a specific version of Alpine for better stability and security updates
FROM alpine:3.18

# Create a non-root user and group
RUN addgroup -S nonroot \
    && adduser -S nonroot -G nonroot

# Switch to the newly created user
USER nonroot

# Set the working directory in the container
WORKDIR /usr/src/app

# Install only necessary packages (Python & pip)
RUN apk add --no-cache python3 py3-pip

# Copy requirements file first for caching benefits
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /usr/src/app

# Set environment variables securely
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the required port
EXPOSE 5000

# Apply security restrictions
SECURITY_OPT ["no-new-privileges:true"]

# Define the entrypoint (Replace "id" with actual application start)
ENTRYPOINT ["python", "app.py"]
