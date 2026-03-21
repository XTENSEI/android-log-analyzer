#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

BINARY="src/core/target/release/loganalyzer"

if [ ! -f "$BINARY" ]; then
    echo "Building core engine..."
    make build-core
fi

echo "=== Benchmarking Android Log Analyzer ==="
echo ""

TEST_FILE="${1:-tests/test.log}"

if [ ! -f "$TEST_FILE" ]; then
    echo "Test file not found: $TEST_FILE"
    exit 1
fi

echo "File: $TEST_FILE"
FILE_SIZE=$(du -h "$TEST_FILE" | cut -f1)
echo "Size: $FILE_SIZE"
echo ""

echo "Running analysis..."
echo ""

for i in 1 2 3; do
    echo "Run $i:"
    START=$(date +%s.%N)
    $BINARY "$TEST_FILE" --output json > /dev/null 2>&1
    END=$(date +%s.%N)
    DIFF=$(echo "$END - START" | bc)
    echo "  Time: ${DIFF}s"
done

echo ""
echo "Benchmark complete"
