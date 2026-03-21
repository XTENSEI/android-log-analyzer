import os
import sys

def ensure_directories():
    dirs = [
        "bin",
        "bin/web",
        "logs",
        "output",
        "temp"
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"Created: {d}/")

def main():
    print("Creating project directories...")
    ensure_directories()
    print("Done!")

if __name__ == "__main__":
    main()
