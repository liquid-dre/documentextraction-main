# Use the base image
FROM python:3.12-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    default-jdk \
    gcc \
    build-essential \
    curl \
    wget \
    cmake \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt
COPY requirements.txt /app/

# Install Cython separately (if needed)
RUN pip install --no-cache-dir Cython==3.0.10

# Install the remaining packages within the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container
COPY . /app

# Make port 8001 available to the world outside this container
EXPOSE 8001

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
