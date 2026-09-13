from typing import Any, Optional
from pydantic import BaseModel, Field

class ScenarioSchema(BaseModel):
    id: str
    title: str
    severity: str
    description: str
    symptoms: str
    affected_services: list[str] = Field(default_factory=list)
    adaptation_flow: Optional[str] = None

class InjectScenarioRequest(BaseModel):
    scenario_id: str = "bad_deployment"
