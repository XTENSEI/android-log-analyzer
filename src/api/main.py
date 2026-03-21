import os
import subprocess
import json
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Log Analyzer API", version="1.0.0")

BINARY_PATH = os.environ.get("LOGANALYZER_BIN", "../core/target/release/loganalyzer")

class AnalysisResponse(BaseModel):
    success: bool
    result: Optional[dict] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Android Log Analyzer API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_log(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    temp_path = Path("/tmp") / file.filename
    try:
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        result = subprocess.run(
            [BINARY_PATH, str(temp_path), "--output", "json"],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            return AnalysisResponse(
                success=False,
                error=result.stderr
            )

        try:
            parsed_result = json.loads(result.stdout)
            return AnalysisResponse(success=True, result=parsed_result)
        except json.JSONDecodeError as e:
            return AnalysisResponse(
                success=False,
                error=f"Failed to parse result: {str(e)}"
            )

    except subprocess.TimeoutExpired:
        return AnalysisResponse(success=False, error="Analysis timeout")
    except Exception as e:
        return AnalysisResponse(success=False, error=str(e))
    finally:
        if temp_path.exists():
            temp_path.unlink()

@app.get("/rules")
async def list_rules():
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
    return {"rules": rules}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
