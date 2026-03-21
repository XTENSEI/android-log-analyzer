#!/usr/bin/env python3
import subprocess
import json
import sys
import os

LOG_FILE = "tests/test.log"
BINARY = "src/core/target/release/loganalyzer"

def run_analysis():
    result = subprocess.run(
        [BINARY, LOG_FILE, "--output", "json"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    
    return json.loads(result.stdout)

def test_total_entries(result):
    assert result["total_entries"] > 0, "Should have parsed some entries"
    print(f"✓ Total entries: {result['total_entries']}")

def test_error_count(result):
    assert result["error_count"] > 0, "Should have detected errors"
    print(f"✓ Error count: {result['error_count']}")

def test_issues_found(result):
    assert len(result["issues"]) > 0, "Should have found issues"
    print(f"✓ Issues found: {len(result['issues'])}")

def test_scan_time(result):
    assert result["scan_time_ms"] > 0, "Should have recorded scan time"
    print(f"✓ Scan time: {result['scan_time_ms']}ms")

def main():
    if not os.path.exists(BINARY):
        print("Binary not found. Please build first.")
        sys.exit(1)
    
    print("Running tests...\n")
    
    result = run_analysis()
    
    test_total_entries(result)
    test_error_count(result)
    test_issues_found(result)
    test_scan_time(result)
    
    print("\n✓ All tests passed!")

if __name__ == "__main__":
    main()
