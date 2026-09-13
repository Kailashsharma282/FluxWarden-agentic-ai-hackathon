import os
from typing import Any, Literal, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FluxWarden"
    TAGLINE: str = "AI that doesn't just detect failure. It adapts and restores."
    PARTICIPANT_NAME: str = "Pochiraju Kailash Ram Markandeya Sharma"
    TEAM_NAME: str = "kailashsharma8"
    HACKATHON_NAME: str = "Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", 8001))
    DEBUG: bool = True
    CORS_ORIGINS: Union[list[str], str] = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, list):
            return [str(item) for item in v]
        if isinstance(v, str):
            v = v.strip()
            if not v or v == "*":
                return ["*"]
            if v.startswith("[") and v.endswith("]"):
                try:
                    import json
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return [str(x) for x in parsed]
                except Exception:
                    pass
            if "," in v:
                return [x.strip() for x in v.split(",") if x.strip()]
            return [v]
        return ["*"]

    # Agent Limits (Configurable as per spec)
    MAX_AGENT_STEPS: int = 15
    MAX_REPLAN_ATTEMPTS: int = 3
    MAX_TOOL_RETRIES: int = 2

    # LLM Configuration
    LLM_PROVIDER: Literal["mock", "openai", "gemini", "anthropic"] = "mock"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Storage Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./fluxwarden.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
