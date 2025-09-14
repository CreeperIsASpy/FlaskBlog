#!/bin/bash
set -e

echo "--- Running Build Script ---"
pip install -r requirements.txt
echo "--- Dependencies Installed. Initializing Database... ---"
flask init-db
echo "--- Database Initialized. ---"