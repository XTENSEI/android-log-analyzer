#!/bin/bash
# Wrapper script for running sepolicy patcher

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

python3 -m src.sepolicy.cli "$@"
