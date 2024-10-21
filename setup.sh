#!/bin/bash

# Create virtual environment
python -m venv venv

#  Activate virtual environment (for Windows Git Bash / MinGW)
source venv/Scripts/activate

# Upgrade pip
# pip install --upgrade pip


# Download spaCy model
python -m spacy download en_core_web_sm

# Install requirements
pip install -r requirements.txt


echo -e "\nSetup complete. \nNow Run 'source venv/Scripts/activate' to activate the virtual environment."
