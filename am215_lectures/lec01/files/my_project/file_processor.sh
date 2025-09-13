#!/usr/bin/env bash
# Script that processes files in a directory

DIRECTORY=${1:-.}  # Use first argument or current directory

echo "Processing files in: $DIRECTORY"
echo "===================="

for file in "$DIRECTORY"/*.txt; do
    if [ -f "$file" ]; then
        echo "File: $(basename "$file")"
        echo "  Lines: $(wc -l < "$file")"
        echo "  Words: $(wc -w < "$file")"
        echo "  Size: $(ls -lh "$file" | awk '{print $5}')"
        echo ""
    fi
done

echo "Processing complete!"
