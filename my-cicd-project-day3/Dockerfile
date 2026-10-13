
# Use an official Python image as the base image.
FROM python:3.13-slim

# Set /app as the working directory inside the container.
WORKDIR /app

# Tell our Flask application to listen on all container interfaces.
# This allows connections forwarded to the container to reach Flask.
ENV APP_HOST=0.0.0.0

# Copy the dependency list into the container first.
COPY requirements.txt .

# Install the Python packages required by our application.
# --no-cache-dir avoids keeping pip's download cache in the image.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code and other build-context files.
# Make sure .dockerignore excludes unnecessary files.
COPY . .

# Document that the application listens on port 5000.
# EXPOSE alone does not publish the port to your host.
EXPOSE 5000

# Start the Flask application when the container launches.
CMD ["python", "app.py"]

