#!/bin/bash

# Navigate to the directory containing the script
cd "$(dirname "$0")"

# Run the Python script
. /home/sunjoo/work/rbp-controller/venv/bin/activate
python3 ina219-data-exporter.py "$@"
