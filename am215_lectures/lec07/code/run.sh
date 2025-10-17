#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="am215-lec05-packaging"

echo "--- Dropping into container; port 8000 is open to host ---"
docker run --rm -it \
  -p 8000:8000 \
  "$IMAGE_NAME" \
  /bin/bash
