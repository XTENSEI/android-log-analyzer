# Android Log Analyzer

A high-performance, multi-language Android log analyzer optimized for large log files (50MB-500MB).

## Architecture

- **Core Engine**: Rust - Streaming log parsing and analysis
- **CLI**: Go - Fast binary distribution
- **API**: Python FastAPI - HTTP interface
- **Web UI**: Vanilla JS - Lightweight frontend

## Performance

- Streaming-based parsing (doesn't load entire file into memory)
- O(n) complexity for log parsing
- Memory-efficient data structures

## Building

See BUILD.md for detailed build instructions.
