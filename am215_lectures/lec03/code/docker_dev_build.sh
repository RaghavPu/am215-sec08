#!/usr/bin/env bash
# Build the development Docker image for Lecture 3.

set -euo pipefail

# The name and tag for the development image
IMAGE_NAME="am215-lec03-dev:latest"

echo "=== Building Development Image: $IMAGE_NAME ==="
echo

# Build the image using Dockerfile.dev in the current directory
docker build -t "$IMAGE_NAME" -f Dockerfile.dev .

echo
echo "=== Build complete! ==="
echo "You can now run the development environment with ./docker_dev_run.sh"
