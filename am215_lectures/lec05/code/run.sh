#!/usr/bin/env bash
set -euo pipefail

# This script starts an interactive session inside the pre-built Docker container.

IMAGE_NAME="am215-lec05-packaging"

echo "--- Starting interactive demo session inside the container ---"
echo "You will be dropped into a bash shell. Follow the instructions in the READMEs."
# Path to your token on the host machine
HOST_TOKEN_PATH="$HOME/.secrets/test-pypi-token"

DOCKER_EXTRA_ARGS=()
# Check if the token file exists on the host
if [ ! -f "$HOST_TOKEN_PATH" ]; then
    echo "Warning: TestPyPI token not found at $HOST_TOKEN_PATH"
    echo "The upload demo step will require manual password entry."
else
    # Read the token from the host file and pass it directly as environment variables.
    DOCKER_EXTRA_ARGS=(
        -e "TWINE_USERNAME=__token__"
        -e "TWINE_PASSWORD=$(cat "$HOST_TOKEN_PATH")"
        -e "UV_PUBLISH_TOKEN=$(cat "$HOST_TOKEN_PATH")"
    )
fi

# Find the Docker socket, preferring the rootless path if it exists.
DOCKER_SOCKET_PATH=""
if [ -S "${XDG_RUNTIME_DIR:-}/docker.sock" ]; then
    DOCKER_SOCKET_PATH="${XDG_RUNTIME_DIR}/docker.sock"
elif [ -S "/var/run/docker.sock" ]; then
    DOCKER_SOCKET_PATH="/var/run/docker.sock"
else
    echo "Error: Could not find an active Docker socket." >&2
    exit 1
fi

# Get the Docker group ID from the host to grant socket permissions.
# Fall back to the current user's group if 'docker' group doesn't exist (common in rootless setups).
DOCKER_GID=$(getent group docker | cut -d: -f3 || echo "")

docker run --rm -it \
    -e DISPLAY="$DISPLAY" \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$DOCKER_SOCKET_PATH":/var/run/docker.sock \
    --group-add "${DOCKER_GID:-$(id -g)}" \
    "${DOCKER_EXTRA_ARGS[@]}" \
    -w /app "$IMAGE_NAME" /bin/bash
