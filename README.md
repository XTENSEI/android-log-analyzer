# Android Log Analyzer

A high-performance, multi-language Android log analyzer built with Rust core, Go CLI, Python FastAPI, and Vanilla JS.

## Quick Start

```bash
# Build everything
make build

# Run analysis
./src/core/target/release/loganalyzer tests/test.log

# Start API
make run-api

# Start web UI
make run-web
```

## Architecture

- **Core Engine** (Rust): High-performance streaming log parser
- **CLI** (Go): Fast command-line interface
- **API** (Python): HTTP API with FastAPI
- **Web UI** (Vanilla JS): Browser-based interface

## Features

- Streaming-based parsing for large files (50MB-500MB)
- Rule-based issue detection
- Multi-log correlation
- JSON/CSV export
- Web-based analysis UI

## Documentation

- [BUILD.md](BUILD.md) - Build instructions
- [src/core/README.md](src/core/README.md) - Core engine details
- [src/cli/README.md](src/cli/README.md) - CLI usage
- [src/api/README.md](src/api/README.md) - API documentation
