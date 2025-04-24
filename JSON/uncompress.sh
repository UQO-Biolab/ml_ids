#!/bin/bash

# Decompress all .tar.gz files in the current directory
for archive in *.tar.gz; do
    tar -xzf "$archive"
done

echo "Decompression completed."
