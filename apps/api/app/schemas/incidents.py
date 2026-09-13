from typing import Any, Optional
from pydantic import BaseModel, Field

class CreateIncidentRequest(BaseModel):
    goal: str = Field(default="The payment API is failing. Investigate the cause and restore service without causing data loss.")
    incident_id: Optional[str] = None
    severity: str = "HIGH"

class ApprovalActionRequest(BaseModel):
    reason: Optional[str] = "Approved by human operator"

class IncidentResponse(BaseModel):
    id: str
    title: str
    goal: str
    status: str
    severity: str
    service: str
    created_at: str
    summary: Optional[str] = None
