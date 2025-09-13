#!/usr/bin/env bash
# Reset script to restore all example files to their original state
# Run this before each lecture presentation

set -e

echo "Resetting lecture example files..."

# Remove existing files directory if it exists
if [ -d "files" ]; then
    rm -rf files
    echo "Removed existing files directory"
fi

# Create directory structure
mkdir -p files/{my_project,logs,config,practice}
echo "Created directory structure"

# Create sample data file
cat > files/sample_data.txt << 'EOF'
Line 1: This is the first line
Line 2: Here's some sample data
Line 3: More content for demonstration
Line 4: We can use this for head/tail examples
Line 5: This file has multiple lines
Line 6: Perfect for learning file commands
Line 7: Each line is numbered for clarity
Line 8: This helps with understanding output
Line 9: Almost at the end now
Line 10: This is the final line
EOF

# Create log file
cat > files/logs/app.log << 'EOF'
2024-09-05 10:30:15 INFO Application started
2024-09-05 10:30:16 DEBUG Loading configuration
2024-09-05 10:30:17 INFO Database connection established
2024-09-05 10:30:18 WARN Deprecated API endpoint used
2024-09-05 10:30:19 ERROR Failed to process request
2024-09-05 10:30:20 INFO Request processed successfully
EOF

# Create config file
cat > files/config/settings.conf << 'EOF'
# Application Configuration
database_host=localhost
database_port=5432
debug_mode=true
log_level=INFO
max_connections=100
EOF

# Create project README
cat > files/my_project/README.md << 'EOF'
# My First Project

This is a sample project directory for the Linux lecture.
EOF

# Create Python script
cat > files/my_project/script.py << 'EOF'
#!/usr/bin/env python3
print('Hello, Linux!')
EOF

# Create hello script
cat > files/my_project/hello_script.sh << 'EOF'
#!/usr/bin/env bash
# Simple greeting script

echo "Hello from my first shell script!"
echo "Today is $(date)"
echo "You are running this script from: $(pwd)"
EOF

# Create greet user script
cat > files/my_project/greet_user.sh << 'EOF'
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
EOF

# Create file processor script
cat > files/my_project/file_processor.sh << 'EOF'
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
EOF

# Make scripts executable
chmod +x files/my_project/*.sh

echo "All example files have been reset to their original state!"
echo "Files are now organized in the 'files/' directory"
echo ""
echo "Directory structure:"
find files -type f | sort
