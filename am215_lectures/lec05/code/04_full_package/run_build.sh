#!/usr/bin/env bash
set -euo pipefail

# This script runs the manylinux build container to produce the wheel.
# It uses docker cp to move files into and out of a temporary build container.

IMAGE_NAME="am215-lec05-card-games-build"

echo "--- Running manylinux build container ---"

# Create a temporary container from the build image
BUILD_CONTAINER=$(docker create "$IMAGE_NAME")

# Copy the source code (the current directory) into the container
docker cp . "$BUILD_CONTAINER":/app

# Run the build by starting the container and waiting for it to complete
docker start -a "$BUILD_CONTAINER"

# Copy the build artifacts from the container back to the current directory
docker cp "$BUILD_CONTAINER":/app/dist .

# Clean up the temporary container
docker rm "$BUILD_CONTAINER" > /dev/null

echo "--- Build complete. sdist and wheel are in the dist/ directory. ---"
