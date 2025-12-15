from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class BatchInfo(BaseModel):
    batch_id: str
    product: str
    status: str
    qc_failure_description: str

class SensorDeviation(BaseModel):
    parameter: str
    normal_value: float
    deviated_value: float
    timestamp_start: str
    timestamp_end: str
    duration_minutes: int

class Evidence(BaseModel):
    deviation: SensorDeviation
    data_points_analyzed: str
    material_lot_correlated: str

class RootCause(BaseModel):
    material_lot: str
    failure_mechanism: str
    scientific_explanation: str

class Recommendation(BaseModel):
    priority: str
    action: str
    description: str

class DeviationReport(BaseModel):
    batch_info: BatchInfo
    evidence: Evidence
    root_cause: RootCause
    recommendations: List[Recommendation]
    timestamp: datetime