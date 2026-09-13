from typing import Any, Optional
from pydantic import BaseModel, Field

class SystemServiceSchema(BaseModel):
    name: str
    display_name: str
    type: str
    status: str
    health_score: int
    version: str
    cpu: int
    memory: int
    error_rate: float
    latency_ms: int
    request_rate: int
    dependencies: list[str] = Field(default_factory=list)
    configuration: dict[str, Any] = Field(default_factory=dict)
    active_target: bool = True

class MetricsSnapshotSchema(BaseModel):
    timestamp: str
    request_rate: int
    error_rate: float
    latency_ms: int
    cpu_usage: int
    memory_usage: int
    active_connections: int
    healthy_services: int
    total_services: int

class SystemStatusResponse(BaseModel):
    overall_status: str
    healthy_services: int
    total_services: int
    traffic_target: str
    active_scenario: Optional[str] = None
    timestamp: str
    project: str
    team: str
    lead: str
    hackathon: str

class SystemSettingsResponse(BaseModel):
    llm_provider: str
    has_openai_key: bool
    has_gemini_key: bool
    has_anthropic_key: bool
    max_agent_steps: int
    max_replan_attempts: int
    max_tool_retries: int

class SystemSettingsUpdateRequest(BaseModel):
    llm_provider: Optional[str] = None
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    max_agent_steps: Optional[int] = None
    max_replan_attempts: Optional[int] = None
    max_tool_retries: Optional[int] = None
