#!/usr/bin/env bash
# Script that uses command line arguments

if [ $# -eq 0 ]; then
    echo "Usage: $0 <name>"
    echo "Please provide your name as an argument"
    exit 1
fi

NAME=$1
TIME=$(date +%H)

if [ $TIME -lt 12 ]; then
    GREETING="Good morning"
elif [ $TIME -lt 18 ]; then
    GREETING="Good afternoon"
else
    GREETING="Good evening"
fi

echo "$GREETING, $NAME!"
echo "Welcome to shell scripting!"
