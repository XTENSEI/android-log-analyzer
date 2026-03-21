.PHONY: all build build-core build-cli build-api build-web clean test help install run-api

BIN_DIR := bin
CORE_DIR := src/core
CLI_DIR := src/cli
API_DIR := src/api
WEB_DIR := src/web

all: build

build: build-core build-cli build-api build-web

build-core:
	@echo "Building Rust core engine..."
	cd $(CORE_DIR) && cargo build --release
	@mkdir -p $(BIN_DIR)
	@cp $(CORE_DIR)/target/release/loganalyzer $(BIN_DIR)/
	@echo "Core engine built successfully"

build-cli:
	@echo "Building Go CLI..."
	cd $(CLI_DIR) && go build -o ../../$(BIN_DIR)/loganalyzer-cli .
	@echo "CLI built successfully"

build-api:
	@echo "Python API dependencies..."
	cd $(API_DIR) && pip install -r requirements.txt -q
	@echo "API dependencies installed"

build-web:
	@echo "Web UI ready (static files)"
	@mkdir -p $(BIN_DIR)/web
	@cp $(WEB_DIR)/*.html $(WEB_DIR)/*.css $(WEB_DIR)/*.js $(BIN_DIR)/web/ 2>/dev/null || true
	@echo "Web UI prepared"

test: build-core
	@echo "Running tests..."
	cd $(CORE_DIR) && cargo test

clean:
	@echo "Cleaning build artifacts..."
	cd $(CORE_DIR) && cargo clean
	rm -rf $(BIN_DIR)
	rm -rf $(API_DIR)/__pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Clean complete"

install: build
	@echo "Installing to /usr/local/bin..."
	cp $(BIN_DIR)/loganalyzer /usr/local/bin/
	cp $(BIN_DIR)/loganalyzer-cli /usr/local/bin/
	@echo "Installation complete"

run-api: build-api
	@echo "Starting API server..."
	cd $(API_DIR) && LOGANALYZER_BIN=../$(BIN_DIR)/loganalyzer python3 main.py

run-web: build-web
	@echo "Starting web server..."
	cd $(BIN_DIR)/web && python3 -m http.server 8080

help:
	@echo "Android Log Analyzer - Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  build       - Build all components"
	@echo "  build-core  - Build Rust core engine only"
	@echo "  build-cli   - Build Go CLI only"
	@echo "  build-api   - Install Python API dependencies"
	@echo "  build-web   - Prepare web UI files"
	@echo "  test        - Run tests"
	@echo "  clean       - Clean build artifacts"
	@echo "  install     - Install binaries to /usr/local/bin"
	@echo "  run-api     - Start API server"
	@echo "  run-web     - Start web server"
	@echo "  help        - Show this help message"
