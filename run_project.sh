#!/bin/bash

# Activate virtual environment (for Windows Git Bash / MinGW)
source venv/Scripts/activate

# Run the main script
python src/main.py

echo "Project execution complete. Check the 'data/processed' folder for the output UML diagram."
