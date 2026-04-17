# Use a stable Python base
FROM python:3.9-slim

# Install system dependencies
# librdkafka-dev is required for confluent-kafka to interface with Kafka
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy and install Python dependencies
# Using --no-cache-dir keeps the image size small
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure logs are sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED=1
