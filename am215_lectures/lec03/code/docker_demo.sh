#!/bin/bash
# Demonstrate Docker workflow for reproducibility

echo "=== Docker Reproducibility Demo ==="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker to run this demo."
    exit 1
fi

echo "1. Building Docker image from 'Dockerfile'..."
docker build -t mc-sim .

echo ""
echo "2. Running analysis in container..."
docker run --rm mc-sim

echo ""
echo "3. Checking image size..."
docker images mc-sim --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Clean up
docker rmi mc-sim >/dev/null 2>&1

echo ""
echo "Demo complete. Docker image removed."
