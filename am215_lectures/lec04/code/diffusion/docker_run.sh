#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="am215/lec04-sim"

echo "Running simulation in ${IMAGE_NAME}..."
# The -v flag mounts the current directory to save the output gif
docker run --rm -v "$(pwd)":/app "${IMAGE_NAME}"
echo "Run complete."
