#!/bin/bash
# Build script for Render

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py
