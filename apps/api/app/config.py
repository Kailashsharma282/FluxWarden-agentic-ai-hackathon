import os
from typing import Literal
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
    CORS_ORIGINS: list[str] = ["*"]

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
