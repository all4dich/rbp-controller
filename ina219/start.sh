#!/bin/bash

# Navigate to the directory containing the script
cd "$(dirname "$0")"

# Run the Python script
python3 ina219-data-exporter.py "$@"