import os
import sys
import json
import subprocess
import argparse

def check_dependencies():
    errors = []
    
    if not os.path.exists("src/core/Cargo.toml"):
        errors.append("Rust core not found")
    
    if not os.path.exists("src/core/target/release/loganalyzer"):
        errors.append("Binary not built. Run: make build-core")
    
    if not os.path.exists("src/api/requirements.txt"):
        errors.append("API requirements not found")
    
    if errors:
        print("Dependency check FAILED:")
        for err in errors:
            print(f"  - {err}")
        return False
    
    print("Dependency check PASSED")
    return True

def setup():
    print("Setting up development environment...")
    
    os.makedirs("bin", exist_ok=True)
    
    if check_dependencies():
        print("\nSetup complete!")
    else:
        print("\nSetup failed. Please fix the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    setup()
