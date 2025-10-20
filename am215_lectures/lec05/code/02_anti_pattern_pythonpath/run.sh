#!/usr/bin/env bash
set -euo pipefail

# This is an anti-pattern! Do not do this in real projects.
# It creates a hidden dependency in the environment.
export PYTHONPATH="$PWD/card_games_lib"
python3 importer_script.py
