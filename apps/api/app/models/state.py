from typing import Any, Optional
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    incident_id: str
    user_goal: str = ""
    constraints: list[str] = Field(default_factory=list)
    current_phase: str = "IDLE"  # IDLE, UNDERSTAND_GOAL, INVESTIGATE, HYPOTHESIS, PLAN, EXECUTE, EVALUATE, REPLAN, WAITING_FOR_APPROVAL, VERIFY, COMPLETE, FAILED
    observations: list[str] = Field(default_factory=list)
    hypotheses: list[str] = Field(default_factory=list)
    selected_actions: list[str] = Field(default_factory=list)
    completed_actions: list[str] = Field(default_factory=list)
    failed_actions: list[dict[str, Any]] = Field(default_factory=list)
    tool_results: list[dict[str, Any]] = Field(default_factory=list)
    system_state: dict[str, Any] = Field(default_factory=dict)
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    approval_required: bool = False
    pending_approval_action: Optional[dict[str, Any]] = None
    attempt_count: int = 0
    replan_count: int = 0
    resolution_status: str = "UNRESOLVED"  # UNRESOLVED, INVESTIGATING, REPLANNING, VERIFYING, RESOLVED, STILL_UNHEALTHY, ESCALATED, FAILED
    final_report: Optional[dict[str, Any]] = None
    structured_explanation: Optional[dict[str, str]] = None
    # Explanation fields: CURRENT ACTION, WHY, EXPECTED RESULT, RISK, RESULT, ADAPTATION

class StructuredExplanation(BaseModel):
    current_action: str = ""
    why: str = ""
    expected_result: str = ""
    risk: str = "LOW"
    result: str = ""
    adaptation: str = ""
