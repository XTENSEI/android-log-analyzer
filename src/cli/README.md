# Log Analyzer CLI

Command-line interface for the Android Log Analyzer.

## Usage

```bash
loganalyzer <logfile> [options]
```

## Options

- `--input, -i <FILE>` - Input log file
- `--output, -o <FORMAT>` - Output format (json, text, summary)
- `--severity <LEVEL>` - Filter by severity (Critical, High, Medium, Low, Info)
- `--verbose, -v` - Verbose output

## Examples

```bash
# Analyze a log file
loganalyzer /path/to/logcat.txt

# Output as JSON
loganalyzer logcat.txt --output json

# Filter critical issues only
loganalyzer logcat.txt --severity Critical

# Save to file
loganalyzer logcat.txt --output json > results.json
```

## Installation

```bash
# Build the CLI
make build-cli

# Install system-wide
sudo cp bin/loganalyzer-cli /usr/local/bin/
```
