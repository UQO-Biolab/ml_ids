#!/bin/bash

# Compress each file in the current directory into a .tar.gz archive
for file in *; do
    if [ -f "$file" ]; then
        tar -czf "${file}.tar.gz" "$file"
    fi
done

echo "Compression completed."
