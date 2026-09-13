import asyncio
from typing import Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.agents.engine import agent_engine
from app.memory.operational import operational_memory
from app.simulations.environment import sim_env

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

# In-memory store for incidents
incidents_db: dict[str, dict[str, Any]] = {
    "INC-1042": {
        "id": "INC-1042",
        "title": "Payment API Failure & 500 Spike",
        "goal": "The payment API is failing. Investigate the cause and restore service without causing data loss.",
        "status": "UNRESOLVED",
        "severity": "CRITICAL",
        "service": "payment-api",
        "created_at": "Just now"
    }
}

class CreateIncidentRequest(BaseModel):
    goal: str = "The payment API is failing. Investigate the cause and restore service without causing data loss."
    incident_id: Optional[str] = None
    severity: str = "HIGH"

class ApprovalActionRequest(BaseModel):
    reason: Optional[str] = None

@router.post("")
async def create_incident(req: CreateIncidentRequest):
    inc_id = req.incident_id or f"INC-{len(incidents_db) + 1042}"
    record = {
        "id": inc_id,
        "title": f"Incident: {req.goal[:40]}...",
        "goal": req.goal,
        "status": "UNRESOLVED",
        "severity": req.severity,
        "service": "payment-api",
        "created_at": "Just now"
    }
    incidents_db[inc_id] = record
    await agent_engine.initialize_mission(user_goal=req.goal, incident_id=inc_id)
    return {"incident": record, "state": agent_engine.state}

@router.get("")
async def list_incidents():
    return {"incidents": list(incidents_db.values())}

@router.get("/{id}")
async def get_incident(id: str):
    if id in incidents_db:
        return {"incident": incidents_db[id], "state": agent_engine.state if agent_engine.state and agent_engine.state.incident_id == id else None}
    raise HTTPException(status_code=404, detail="Incident not found")

@router.post("/{id}/start")
async def start_incident(id: str, background_tasks: BackgroundTasks):
    if not agent_engine.state or agent_engine.state.incident_id != id:
        goal = incidents_db.get(id, {}).get("goal", "Investigate and restore payment service")
        await agent_engine.initialize_mission(user_goal=goal, incident_id=id)

    # Launch background autonomous loop
    background_tasks.add_task(agent_engine.run_mission_loop, delay=0.7)
    return {"status": "started", "incident_id": id, "phase": agent_engine.state.current_phase}

@router.post("/{id}/stop")
async def stop_incident(id: str):
    agent_engine.is_running = False
    return {"status": "stopped", "incident_id": id}

@router.get("/{id}/state")
async def get_incident_state(id: str):
    if agent_engine.state and agent_engine.state.incident_id == id:
        return agent_engine.state
    # Fallback to current state if active
    return agent_engine.state or {"incident_id": id, "current_phase": "IDLE", "resolution_status": "UNRESOLVED"}

@router.get("/{id}/events")
async def get_incident_events(id: str):
    return {"events": [e.model_dump() for e in agent_engine.events]}

@router.get("/{id}/trace")
async def get_incident_trace(id: str):
    trace_steps = []
    for idx, e in enumerate(agent_engine.events):
        trace_steps.append({
            "step": idx + 1,
            "time": e.time_display,
            "type": e.type,
            "tool": e.tool,
            "summary": e.summary,
            "severity": e.severity
        })
    return {
        "incident_id": id,
        "total_steps": len(trace_steps),
        "trace": trace_steps,
        "completed_actions": agent_engine.state.completed_actions if agent_engine.state else [],
        "failed_actions": agent_engine.state.failed_actions if agent_engine.state else []
    }

@router.post("/{id}/approve")
async def approve_action(id: str):
    state = await agent_engine.approve_pending_action()
    return {"status": "approved", "state": state}

@router.post("/{id}/reject")
async def reject_action(id: str, req: ApprovalActionRequest = ApprovalActionRequest()):
    state = await agent_engine.reject_pending_action(reason=req.reason or "Rejected by human operator")
    return {"status": "rejected", "state": state}
