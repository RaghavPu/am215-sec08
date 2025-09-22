#!/usr/bin/env bash
# setup.sh - Check for required tools and environment

set -euo pipefail

echo "=== Environment Setup Check ==="
echo

# 1. Check for required commands
echo "1. Checking for required commands..."
MISSING_DEPS=0
for cmd in python3 git; do
    if command -v $cmd >/dev/null 2>&1; then
        echo "  ✓ $cmd found"
    else
        echo "  ✗ $cmd MISSING - please install"
        MISSING_DEPS=1
    fi
done

if [ $MISSING_DEPS -eq 1 ]; then
    echo
    echo "Please install missing dependencies before continuing."
    exit 1
fi
echo

# 2. Check Python version
echo "2. Checking Python version..."
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || [ "$PYTHON_MINOR" -lt 8 ]; then
    echo "  ✗ Python $PYTHON_VERSION is too old. Python 3.8+ required."
    exit 1
elif [ "$PYTHON_VERSION" != "3.10" ]; then
    echo "  ! Warning: Python $PYTHON_VERSION found. Python 3.10 recommended for exact reproducibility."
else
    echo "  ✓ Python $PYTHON_VERSION"
fi
echo

# 3. Check for environment files
echo "3. Checking for environment definition files..."
MISSING_FILES=0
for f in requirements.txt environment.yml Dockerfile; do
    if [ -f "$f" ]; then
        echo "  ✓ $f found"
    else
        echo "  ✗ $f MISSING"
        MISSING_FILES=1
    fi
done

if [ $MISSING_FILES -eq 1 ]; then
    echo
    echo "Some environment files are missing. Please ensure all files are present."
    exit 1
fi
echo

echo "=== Setup check complete! ==="
echo
echo "You can now create an environment using:"
echo "  • Virtual env:  ./venv_demo.sh"
echo "  • Conda:        conda env create -f environment.yml"
echo "  • Docker:       ./docker_demo.sh"
