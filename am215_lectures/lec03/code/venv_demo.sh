#!/usr/bin/env bash
# 03_demo_venv.sh - Demonstrate virtual environment isolation

set -euo pipefail

echo "=== Virtual Environment Demo ==="
echo

# Clean up any existing environment
if [ -d "demo_env" ]; then
    echo "Removing existing demo_env..."
    rm -rf demo_env
fi

# Create fresh virtual environment
echo "1. Creating virtual environment..."
python3 -m venv demo_env

echo "2. Activating environment..."
source demo_env/bin/activate

echo "3. Checking Python location:"
which python
echo

echo "4. Initial package list (should be minimal):"
pip list
echo

echo "5. Installing requirements..."
pip install -q -r requirements-pinned.txt
echo

echo "6. Updated package list:"
pip list
echo

echo "7. Checking sys.path in Python:"
python -c "import sys; print('\n'.join(sys.path[:3]))"
echo

echo "8. Running simulation in venv..."
python mc_simulation.py

echo
echo "Demo complete. To deactivate, run: deactivate"
echo "To clean up, run: rm -rf demo_env walk_analysis.png"
