from typing import Optional, List
from pydantic import BaseModel

class LogEntry(BaseModel):
    timestamp: int
    level: str
    tag: str
    pid: int
    tid: int
    message: str
    line_number: int

class Issue(BaseModel):
    rule_id: str
    severity: str
    category: str
    message: str
    tag: str
    line_number: int
    count: int

class AnalysisResult(BaseModel):
    total_entries: int
    error_count: int
    warning_count: int
    info_count: int
    debug_count: int
    tags: dict
    issues: List[Issue]
    issues_by_severity: dict
    issues_by_category: dict
    top_tags: List[tuple]
    scan_time_ms: int

class AnalyzeRequest(BaseModel):
    min_severity: Optional[str] = None
    filter_tag: Optional[str] = None
    search_text: Optional[str] = None

class AnalyzeResponse(BaseModel):
    success: bool
    result: Optional[AnalysisResult] = None
    error: Optional[str] = None

class RuleInfo(BaseModel):
    id: str
    name: str
    severity: str
    category: str
    description: str

class HealthResponse(BaseModel):
    status: str
    version: str
    core_binary: str
