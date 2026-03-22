# Android Log Analyzer

A high-performance, multi-language Android log analyzer built with Rust core, Python Flask API, and Vanilla JS web UI.

## Quick Start

```bash
# Build everything
make build

# Run log analysis (Rust)
./bin/loganalyzer tests/test.log

# Run SELinux AVC analyzer (Python)
python3 src/sepolicy/avc_analyzer.py avc_log.txt

# Start API server (Flask, port 8000)
make run-api

# Start web UI (port 8080)
make run-web
```

## Two Main Tools

### 1. Log Analyzer (Rust)

The core streaming log analyzer built in Rust for high-performance analysis of large log files.

```bash
# Basic analysis
./bin/loganalyzer /path/to/logcat.log

# Output as JSON
./bin/loganalyzer /path/to/logcat.log --output json

# Show help
./bin/loganalyzer --help
```

### 2. SELinux AVC Analyzer (Python)

Analyzes SELinux Access Vector Cache (AVC) denials from Android kernel logs.

```bash
# Analyze AVC denials
python3 src/sepolicy/avc_analyzer.py avc_log.txt

# Generate HTML report
python3 src/sepolicy/avc_analyzer.py avc_log.txt --html report.html

# Compare two AVC logs
python3 src/sepolicy/avc_analyzer.py avc_old.txt avc_new.txt --compare
```

## Architecture

- **Core Engine** (Rust): High-performance streaming log parser in `src/core/`
- **API** (Python Flask): HTTP API at `src/api/main.py` (port 8000)
- **SELinux Analyzer** (Python): AVC denial analyzer in `src/sepolicy/`
- **Web UI** (Vanilla JS): Browser-based interface in `src/web/`

## Features

- Streaming-based parsing for large files (50MB-500MB)
- Rule-based issue detection (ANR, CRASH, NPE, OOM, WTF, etc.)
- Multi-log correlation
- JSON/CSV export
- SELinux AVC denial analysis with risk assessment
- Root cause analysis for AVC denials
- Policy fix suggestions
- HTML report generation
- Web-based analysis UI

## Example Output

### Log Analyzer Output

```json
{
  "summary": {
    "total_lines": 15234,
    "errors": 42,
    "warnings": 156,
    "issues_found": 8
  },
  "issues": [
    {
      "type": "ANR",
      "message": "ANR in com.example.app",
      "timestamp": "2024-01-15T10:23:45Z",
      "severity": "Critical"
    },
    {
      "type": "CRASH",
      "message": "java.lang.NullPointerException",
      "timestamp": "2024-01-15T10:24:12Z",
      "severity": "Critical"
    }
  ]
}
```

### AVC Analyzer Output

```json
{
  "total_denials": 15,
  "by_risk_level": {
    "CRITICAL": 2,
    "HIGH": 5,
    "MEDIUM": 6,
    "LOW": 2
  },
  "statistics": {
    "by_source": {
      "untrusted_app": 8,
      "system_server": 4,
      "hal_fingerprint": 3
    }
  }
}
```

## Build Instructions

### Prerequisites

- Rust (for core engine)
- Python 3.x
- Flask (`pip install flask`)

### Build Steps

```bash
# Install Rust if needed
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Python dependencies
pip install flask

# Build all components
make build

# Or build individual components
make build-core    # Rust log analyzer
make build-api     # Flask API dependencies
make build-web     # Web UI files
```

### Running the API

```bash
# Start the Flask API server (port 8000)
make run-api

# Or manually:
cd src/api
python3 main.py
```

The API provides:
- `GET /` - API info
- `GET /health` - Health check
- `POST /analyze` - Upload and analyze log file
- `GET /rules` - List detection rules

### Running the Web UI

```bash
# Start web server (port 8080)
make run-web

# Open in browser
# http://localhost:8080
```

## Documentation

- [BUILD.md](BUILD.md) - Detailed build instructions
- [src/core/](src/core/) - Rust core engine
- [src/sepolicy/](src/sepolicy/) - SELinux AVC analyzer
