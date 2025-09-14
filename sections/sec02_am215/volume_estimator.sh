#!/bin/bash
set -euo pipefail

if [ -n "${VIRTUAL_ENV:-}" ]; then
  if [ -x "$VIRTUAL_ENV/Scripts/python.exe" ]; then PY="$VIRTUAL_ENV/Scripts/python.exe"; fi
  if [ -x "$VIRTUAL_ENV/bin/python" ]; then PY="$VIRTUAL_ENV/bin/python"; fi
fi
if [ -z "${PY:-}" ] && command -v python3 >/dev/null 2>&1; then PY=python3; fi
if [ -z "${PY:-}" ] && command -v py >/dev/null 2>&1; then PY="py -3"; fi
if [ -z "${PY:-}" ] && command -v python >/dev/null 2>&1; then PY=python; fi
if [ -z "${PY:-}" ]; then echo "No Python interpreter found"; exit 1; fi

while true; do
  read -p "Enter dimension: " dimension
  read -p "Enter maximum number of points: " max_points
  read -p "Enter number of simulations: " num_sim
  for ((i=1; i<=num_sim; i++)); do
    $PY hypersphere_volume.py "$dimension" "$max_points" >> results.csv
  done
  read -p "Run another estimation? (y/n): " again
  [ "$again" = "y" ] || break
done
