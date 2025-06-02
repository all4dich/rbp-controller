#!/bin/bash

# Navigate to the directory containing the script
cd "$(dirname "$0")"

# Run the Python script
. /home/sunjoo/work/rbp-controller/venv/bin/activate
python3 ina260-data-exporter.py --device nvidia-agx-orig "$@"
