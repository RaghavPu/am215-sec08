#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="am215/lec04-sim"

echo "Building ${IMAGE_NAME}..."
docker build -t "${IMAGE_NAME}" .
echo "Build complete."
