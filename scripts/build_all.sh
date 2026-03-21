#!/bin/bash

echo "=== Building all components ==="

echo ""
echo "Step 1: Building Rust core..."
make build-core

echo ""
echo "Step 2: Building Go CLI..."
make build-cli

echo ""
echo "Step 3: Setting up Python API..."
make build-api

echo ""
echo "Step 4: Preparing Web UI..."
make build-web

echo ""
echo "=== Build complete ==="
echo ""
echo "Run './scripts/start.sh' to start the API server"
