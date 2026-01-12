#!/bin/bash

# Deployment script for Wisdom Extractor
# This script automates the deployment process for the Wisdom Extractor application.
# It includes steps for building, testing, and deploying the application.

# Exit immediately if any command fails
set -e

# Function to display error messages
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Docker is installed
if ! command_exists docker; then
    error_exit "Docker is not installed. Please install Docker and try again."
fi

# Check if Docker Compose is installed
if ! command_exists docker-compose; then
    error_exit "Docker Compose is not installed. Please install Docker Compose and try again."
fi

# Build the Docker image
echo "Building Docker image..."
docker build -t wisdom-extractor -f deployment/Dockerfile . || error_exit "Failed to build Docker image."

# Run tests
echo "Running tests..."
docker run wisdom-extractor pytest || error_exit "Tests failed."

# Deploy the application
echo "Deploying the application..."
docker-compose -f deployment/docker-compose.yml up -d || error_exit "Failed to deploy the application."

echo "Deployment completed successfully!"
