from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    ERROR = "error"

class TaskStatus(BaseModel):
    task_name: str
    status: StatusEnum
    output: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class AgentStatus(BaseModel):
    agent_id: str
    agent_name: str
    role: str
    status: StatusEnum
    tasks: List[TaskStatus] = []
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class InvestigationStatus(BaseModel):
    investigation_id: str
    status: StatusEnum
    agents: List[AgentStatus] = []
    started_at: datetime
    completed_at: Optional[datetime] = None
    final_report: Optional[dict] = None
