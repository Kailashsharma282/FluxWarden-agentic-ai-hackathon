import uuid
from datetime import datetime, timezone
from typing import Any, Optional
from pydantic import BaseModel, Field

class AgentEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    incident_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    time_display: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
    type: str  # e.g., GOAL_ACCEPTED, TOOL_SELECTED, ACTION_FAILED, REPLAN_STARTED, etc.
    tool: Optional[str] = None
    summary: str
    severity: str = "info"  # info, warning, error, success, critical
    details: Optional[dict[str, Any]] = None
