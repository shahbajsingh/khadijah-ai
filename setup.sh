#!/bin/bash
# setup.sh

# Create a virtual environment 
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Setup complete."
