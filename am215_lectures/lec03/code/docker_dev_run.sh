#!/usr/bin/env bash
# Run an interactive shell in the Lecture 3 development container.

set -euo pipefail

# The name of the development image to use
IMAGE_NAME="am215-lec03-dev:latest"

echo "=== Starting Development Container from Image: $IMAGE_NAME ==="
echo "Note: Your current directory is mounted at /code inside the container."
echo "The host's Docker socket is mounted to allow running Docker commands."
echo

# Check if the Docker socket exists
if [ ! -S "${XDG_RUNTIME_DIR}/docker.sock" ]; then
    echo "Error: Docker socket not found at ${XDG_RUNTIME_DIR}/docker.sock."
    echo "Is the rootless Docker daemon running on your host?"
    exit 1
fi

# Get the Docker group ID from the host (for Docker socket access)
DOCKER_GID=$(getent group docker | cut -d: -f3 || echo "")

# Run the container as root.
docker run -it --rm \
    --group-add "${DOCKER_GID:-$(id -g)}" \
    -v "$(pwd)":/code \
    -v "${XDG_RUNTIME_DIR}/docker.sock":/var/run/docker.sock \
    -w /code \
    "$IMAGE_NAME" \
    /bin/bash

echo
echo "=== Exited Development Container ==="
