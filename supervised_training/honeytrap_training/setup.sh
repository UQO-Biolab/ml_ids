#!/bin/bash

# Creation of venv
python3 -m venv honeytrap_training

# Linux activation (Other for Win)
source venv/bin/activate

# Install libraries
pip install --upgrade pip
pip install -r requirements.txt

echo "Environment ready! Activate with: source venv/bin/activate"

