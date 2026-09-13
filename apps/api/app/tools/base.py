from typing import Any, Callable, Coroutine, Optional
from pydantic import BaseModel, Field

class ToolDefinition(BaseModel):
    name: str
    description: str
    category: str  # diagnostic, remediation, verification, safety
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    permission_requirements: list[str] = Field(default_factory=lambda: ["operator"])
    timeout_seconds: int = 10
    retry_policy: dict[str, Any] = Field(default_factory=lambda: {"max_retries": 2, "backoff_ms": 500})
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)

class ToolResult(BaseModel):
    tool: str
    success: bool
    data: Any
    error: Optional[str] = None
    execution_time_ms: int = 15
    timestamp: str = ""
