#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=== Android Log Analyzer ==="
echo ""

if [ ! -f "src/core/target/release/loganalyzer" ]; then
    echo "Building core engine..."
    make build-core
fi

echo ""
echo "Starting API server..."
echo "Open http://localhost:8000 in your browser"
echo ""

cd src/api
export LOGANALYZER_BIN=../../src/core/target/release/loganalyzer
python3 main.py
