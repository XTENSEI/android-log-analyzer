import os
import subprocess
import json
from pathlib import Path
from typing import Optional
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='../web')

BINARY_PATH = os.environ.get("LOGANALYZER_BIN", "../core/target/release/loganalyzer")

@app.route("/")
def root():
    return {"message": "Android Log Analyzer API", "version": "1.0.0"}

@app.route("/health")
def health():
    return {"status": "healthy"}

@app.route("/analyze", methods=["POST"])
def analyze_log():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"success": False, "error": "No file provided"}), 400

    temp_path = Path("/tmp") / file.filename
    try:
        with open(temp_path, "wb") as f:
            f.write(file.read())

        result = subprocess.run(
            [BINARY_PATH, str(temp_path), "--output", "json"],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            return jsonify({
                "success": False,
                "error": result.stderr
            })

        try:
            parsed_result = json.loads(result.stdout)
            return jsonify({"success": True, "result": parsed_result})
        except json.JSONDecodeError as e:
            return jsonify({
                "success": False,
                "error": f"Failed to parse result: {str(e)}"
            })

    except subprocess.TimeoutExpired:
        return jsonify({"success": False, "error": "Analysis timeout"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        if temp_path.exists():
            temp_path.unlink()

@app.route("/rules")
def list_rules():
    rules = [
        {"id": "ANR", "name": "Application Not Responding", "severity": "Critical"},
        {"id": "CRASH", "name": "Application Crash", "severity": "Critical"},
        {"id": "NPE", "name": "NullPointerException", "severity": "High"},
        {"id": "OOM", "name": "Out of Memory", "severity": "Critical"},
        {"id": "WTF", "name": "What a Terrible Failure", "severity": "High"},
        {"id": "LOW_MEMORY", "name": "Low Memory Warning", "severity": "Medium"},
        {"id": "SECURITY", "name": "Security Issue", "severity": "High"},
        {"id": "BATTERY", "name": "Battery Issue", "severity": "Medium"},
    ]
    return jsonify({"rules": rules})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
