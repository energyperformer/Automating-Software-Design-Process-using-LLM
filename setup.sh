#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment (for Windows Git Bash / MinGW)
source venv/Scripts/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

echo "Setup complete. Run 'source venv/Scripts/activate' to activate the virtual environment."
