# API Documentation

Base URL: `http://localhost:8000`

## Endpoints

### Health Check
```
GET /health
```

Response:
```json
{
  "status": "healthy"
}
```

### Analyze Log
```
POST /analyze
Content-Type: multipart/form-data
```

Parameters:
- `file`: Log file (required)

Response:
```json
{
  "success": true,
  "result": {
    "total_entries": 1000,
    "error_count": 50,
    "warning_count": 100,
    "issues": [...],
    "scan_time_ms": 150
  }
}
```

### List Rules
```
GET /rules
```

Response:
```json
{
  "rules": [
    {
      "id": "ANR",
      "name": "Application Not Responding",
      "severity": "Critical"
    }
  ]
}
```

## Web UI

The web UI is served at `/` when the API is running.

Upload a log file via the web interface to analyze it visually.
