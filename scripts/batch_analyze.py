import os
import sys
import json
import subprocess
import glob

def find_logs(directory):
    patterns = ["*.log", "*.txt", "logcat*", "bugreport*"]
    logs = []
    
    for pattern in patterns:
        logs.extend(glob.glob(os.path.join(directory, "**", pattern), recursive=True))
    
    return logs

def analyze_all(logs, binary):
    results = []
    
    for log in logs:
        print(f"Analyzing: {log}")
        result = subprocess.run(
            [binary, log, "--output", "json"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                results.append({
                    "file": log,
                    "data": data
                })
            except:
                pass
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: batch_analyze.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    binary = "src/core/target/release/loganalyzer"
    
    if not os.path.exists(binary):
        print(f"Error: Binary not found at {binary}")
        sys.exit(1)
    
    logs = find_logs(directory)
    
    print(f"Found {len(logs)} log files")
    
    results = analyze_all(logs, binary)
    
    output_file = "batch_analysis.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()
