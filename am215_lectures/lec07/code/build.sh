#!/usr/bin/env bash
set -euo pipefail

# This script builds the Docker image for the lecture 5 packaging demos.

IMAGE_NAME="am215-lec05-packaging"

echo "--- Building Docker image: $IMAGE_NAME ---"
docker build -t "$IMAGE_NAME" .
echo "--- Build complete. You can now run the demos with ./run.sh ---"
