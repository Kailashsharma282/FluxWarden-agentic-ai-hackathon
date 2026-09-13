from typing import Any, Optional
from pydantic import BaseModel, Field

class FinalReportSchema(BaseModel):
    title: str
    participant: str
    team: str
    hackathon: str
    incident_id: str
    incident_summary: str
    root_cause: str
    evidence: list[str] = Field(default_factory=list)
    actions_taken: list[str] = Field(default_factory=list)
    failed_actions: list[dict[str, Any]] = Field(default_factory=list)
    adaptation: str
    recovery_strategy: str
    verification_results: dict[str, Any] = Field(default_factory=dict)
    final_state: str = "OPERATIONAL"
    duration_seconds: float = 0.0
    risk_decisions: list[dict[str, Any]] = Field(default_factory=list)
