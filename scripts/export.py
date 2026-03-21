import json
import subprocess
import sys
import os
import argparse

def analyze_and_export(input_file, output_file, format='json'):
    binary = "src/core/target/release/loganalyzer"
    
    if not os.path.exists(binary):
        print(f"Error: Binary not found at {binary}")
        print("Please build the project first: make build-core")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    result = subprocess.run(
        [binary, input_file, "--output", format],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    
    with open(output_file, 'w') as f:
        f.write(result.stdout)
    
    print(f"Analysis complete. Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Android logs and export results")
    parser.add_argument("input", help="Input log file")
    parser.add_argument("output", help="Output file")
    parser.add_argument("--format", choices=["json", "text", "summary"], default="json", 
                        help="Output format")
    
    args = parser.parse_args()
    analyze_and_export(args.input, args.output, args.format)
