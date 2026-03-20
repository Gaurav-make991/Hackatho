from pydantic import BaseModel
from typing import Optional, List

class LogLine(BaseModel):
    id: int
    timestamp: str
    level: str
    service: str
    message: str
    raw: str
    anomaly_score: float = 0.0

class AnomalyResult(BaseModel):
    session_id: str
    total_lines: int
    anomaly_count: int
    peak_score: float
    flagged_lines: List[LogLine]
    status: str

class CrashReport(BaseModel):
    session_id: str
    first_anomalous_event: str
    probable_root_cause: str
    affected_services: List[str]
    timeline: List[dict]
    recommended_fix: str
    anomaly_category: str
    confidence: str

class QueryRequest(BaseModel):
    session_id: str
    question: str

class QueryResponse(BaseModel):
    answer: str
    matching_lines: List[LogLine] = []

class SimilarIncident(BaseModel):
    incident_id: int
    summary: str
    root_cause: str
    resolution: str
    similarity_score: float