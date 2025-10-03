#!/usr/bin/env bash
set -euo pipefail

# This script builds the Docker image for building the manylinux wheel.

IMAGE_NAME="am215-lec05-card-games-build"

echo "--- Building manylinux build image: $IMAGE_NAME ---"
docker build -t "$IMAGE_NAME" .
echo "--- Build complete. ---"
