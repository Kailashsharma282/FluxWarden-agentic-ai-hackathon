from fastapi import APIRouter
from app.simulations.environment import sim_env
from app.config import settings

router = APIRouter(prefix="/api/system", tags=["system"])

@router.get("/status")
async def get_system_status():
    services = sim_env.get_services()
    healthy_count = sum(1 for s in services if s["status"] == "healthy")
    overall = "OPERATIONAL" if healthy_count == len(services) else ("DEGRADED" if healthy_count > len(services) / 2 else "OUTAGE")
    return {
        "overall_status": overall,
        "healthy_services": healthy_count,
        "total_services": len(services),
        "traffic_target": sim_env.traffic_target,
        "active_scenario": sim_env.active_scenario,
        "timestamp": sim_env.get_metrics_snapshot()["timestamp"],
        "project": settings.PROJECT_NAME,
        "team": settings.TEAM_NAME,
        "lead": settings.PARTICIPANT_NAME,
        "hackathon": settings.HACKATHON_NAME
    }

@router.get("/services")
async def get_services():
    return {"services": sim_env.get_services()}

@router.get("/metrics")
async def get_metrics():
    return {"metrics": sim_env.get_metrics_snapshot()}

@router.get("/settings")
async def get_settings():
    return {
        "llm_provider": settings.LLM_PROVIDER,
        "has_openai_key": bool(settings.OPENAI_API_KEY),
        "has_gemini_key": bool(settings.GEMINI_API_KEY),
        "has_anthropic_key": bool(settings.ANTHROPIC_API_KEY),
        "max_agent_steps": settings.MAX_AGENT_STEPS,
        "max_replan_attempts": settings.MAX_REPLAN_ATTEMPTS,
        "max_tool_retries": settings.MAX_TOOL_RETRIES
    }

@router.post("/settings")
async def update_settings(payload: dict):
    from app.agents.engine import agent_engine
    if "llm_provider" in payload and payload["llm_provider"]:
        settings.LLM_PROVIDER = payload["llm_provider"]
    if "openai_api_key" in payload and payload["openai_api_key"]:
        settings.OPENAI_API_KEY = payload["openai_api_key"]
    if "gemini_api_key" in payload and payload["gemini_api_key"]:
        settings.GEMINI_API_KEY = payload["gemini_api_key"]
    if "anthropic_api_key" in payload and payload["anthropic_api_key"]:
        settings.ANTHROPIC_API_KEY = payload["anthropic_api_key"]
    if "max_agent_steps" in payload and payload["max_agent_steps"] is not None:
        settings.MAX_AGENT_STEPS = int(payload["max_agent_steps"])
    if "max_replan_attempts" in payload and payload["max_replan_attempts"] is not None:
        settings.MAX_REPLAN_ATTEMPTS = int(payload["max_replan_attempts"])
    if "max_tool_retries" in payload and payload["max_tool_retries"] is not None:
        settings.MAX_TOOL_RETRIES = int(payload["max_tool_retries"])

    agent_engine.update_provider()

    return {
        "status": "updated",
        "llm_provider": settings.LLM_PROVIDER,
        "has_openai_key": bool(settings.OPENAI_API_KEY),
        "has_gemini_key": bool(settings.GEMINI_API_KEY),
        "has_anthropic_key": bool(settings.ANTHROPIC_API_KEY),
        "max_agent_steps": settings.MAX_AGENT_STEPS,
        "max_replan_attempts": settings.MAX_REPLAN_ATTEMPTS,
        "max_tool_retries": settings.MAX_TOOL_RETRIES
    }
