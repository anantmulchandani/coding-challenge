#!/bin/bash
set -e

echo "Running ingestion and analysis..."
python setup.py

echo "Starting the API server..."
python main.py
