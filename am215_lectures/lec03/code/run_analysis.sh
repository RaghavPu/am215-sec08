#!/usr/bin/env bash
# run_analysis.sh - A reproducible pipeline script for the MC simulation

set -euo pipefail

echo "=== Running Monte Carlo Analysis Pipeline ==="
echo

# Create a directory for results, with a timestamp
RESULTS_DIR="results_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"
echo "1. Created results directory: $RESULTS_DIR"

# Define log file
LOG_FILE="$RESULTS_DIR/run.log"
touch "$LOG_FILE"

# Capture environment details
echo "2. Logging environment details to $LOG_FILE..."
{
    echo "--- Pipeline Run Details ---"
    echo "Timestamp: $(date)"
    echo "User: $(whoami)"
    echo "Host: $(hostname)"
    echo "Directory: $(pwd)"
    echo "----------------------------"
    echo
    
    # Check if git is available and we're in a repo
    if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
        echo "--- Git Status ---"
        git status --short
        git rev-parse HEAD 2>/dev/null || echo "No commits yet"
        echo "------------------"
    else
        echo "--- Git Status ---"
        echo "Not in a git repository or git not available"
        echo "------------------"
    fi
    echo
    
    echo "--- Python Details ---"
    python3 --version
    echo
    echo "--- Installed Packages ---"
    pip list 2>/dev/null || pip3 list
    echo "--------------------------"
    echo
    echo "--- Script Output ---"
} >> "$LOG_FILE"

# Run the simulation and append output to the log
echo "3. Running mc_simulation.py..."
if python3 mc_simulation.py 2>&1 | tee -a "$LOG_FILE"; then
    echo "   ✓ Simulation completed successfully"
else
    echo "   ✗ Simulation failed. Check $LOG_FILE for details."
    exit 1
fi

# Move the output plot to the results directory if it exists
if [ -f "walk_analysis.png" ]; then
    mv walk_analysis.png "$RESULTS_DIR/"
    echo "4. Moved walk_analysis.png to $RESULTS_DIR"
else
    echo "4. Note: walk_analysis.png not found (may be expected in container environment)"
fi
echo

echo "=== Pipeline complete ==="
echo "Results are in: $RESULTS_DIR"
echo "Log file: $LOG_FILE"
