#!/bin/bash

set -e

echo "=== Running Tests ==="

echo ""
echo "Testing Rust core..."
cd src/core
cargo test

echo ""
echo "All tests passed!"
