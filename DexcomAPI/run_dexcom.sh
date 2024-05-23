#!/bin/bash
# Load environment variables
source "/Users/ericspencer/Documents/GitHub/DexcomNumberViewer/DexcomAPI/.env"

# Run the Python script and log the output
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 /Users/ericspencer/Documents/GitHub/DexcomNumberViewer/DexcomAPI/main.py >> /Users/ericspencer/Documents/GitHub/DexcomNumberViewer/DexcomAPI/main.log 2>&1

