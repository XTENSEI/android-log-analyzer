import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

def main():
    print("=== Android Log Analyzer ===")
    print("Version: 1.0.0")
    print("")
    print("Components:")
    print("  - Core: Rust (streaming parser)")
    print("  - API: Python FastAPI")
    print("  - CLI: Go")
    print("  - Web: Vanilla JS")
    print("")

if __name__ == "__main__":
    main()
