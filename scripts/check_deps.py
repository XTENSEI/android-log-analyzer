import sys
import os
import subprocess

def check_rust():
    try:
        result = subprocess.run(["rustc", "--version"], capture_output=True, text=True)
        print(f"✓ Rust: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("✗ Rust not found")
        return False

def check_go():
    try:
        result = subprocess.run(["go", "version"], capture_output=True, text=True)
        print(f"✓ Go: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("✗ Go not found")
        return False

def check_python():
    try:
        result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
        print(f"✓ Python: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("✗ Python not found")
        return False

def main():
    print("Checking development environment...\n")
    
    rust = check_rust()
    go = check_go()
    python = check_python()
    
    if rust and go and python:
        print("\n✓ All dependencies available")
    else:
        print("\n✗ Some dependencies are missing")

if __name__ == "__main__":
    main()
