# Building Android Log Analyzer

## Prerequisites

- Rust (1.70+)
- Go (1.21+)
- Python 3.9+
- pip

## Quick Start

```bash
# Clone and navigate to project
cd android-log-analyzer

# Build all components
make build

# Or build individually
make build-core    # Rust analyzer
make build-cli     # Go CLI
make build-api     # Python API
make build-web     # Web UI
```

## Running

### CLI
```bash
./bin/loganalyzer <logfile> --output json
```

### API Server
```bash
make run-api
# Or manually:
cd src/api
pip install -r requirements.txt
LOGANALYZER_BIN=../core/target/release/loganalyzer python3 main.py
```

### Web UI
```bash
# Serve from the web directory
cd src/web
python3 -m http.server 8080
```

## Development

### Rust Tests
```bash
cd src/core
cargo test
```

### Build Release Binary
```bash
cd src/core
cargo build --release
```

## Performance

The analyzer is optimized for large log files (50MB-500MB):
- Streaming-based parsing
- Memory-efficient
- O(n) complexity
