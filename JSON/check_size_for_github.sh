#!/bin/bash

# Check for .tar.gz files exceeding 100 MB
echo "Checking for .tar.gz files exceeding 100 MB..."

# Use find to search for .tar.gz files larger than 100 MB
large_files=$(find . -maxdepth 1 -name '*.tar.gz' -size +100M)

# Check if any files were found
if [ -z "$large_files" ]; then
    echo "No .tar.gz files exceed 100 MB."
else
    echo "The following files exceed 100 MB:"
    for file in $large_files; do
        ls -lh "$file"
    done
fi
