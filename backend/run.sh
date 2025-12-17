#!/bin/bash
# Run script for Clustering Platform Backend

# Activate virtual environment
if [ -d "../venv" ]; then
    source ../venv/bin/activate
else
    echo "Error: Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Run the application
python run.py

