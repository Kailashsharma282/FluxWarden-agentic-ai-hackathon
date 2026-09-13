from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.engine import agent_engine

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatMessageRequest(BaseModel):
    message: str

@router.post("")
async def send_chat_message(req: ChatMessageRequest):
    user_msg = req.message.strip()

    # If message indicates an incident investigation goal
    if any(keyword in user_msg.lower() for keyword in ["failing", "restore", "investigate", "error", "incident", "fix", "recover"]):
        await agent_engine.initialize_mission(user_goal=user_msg, incident_id="INC-1042")
        response_text = (
            f"Mission accepted.\n\n"
            f"Goal: {user_msg}\n"
            f"Constraint: Preserve data integrity. Zero arbitrary shell execution.\n\n"
            f"Starting autonomous investigation of payment-api and connected infrastructure..."
        )
        return {
            "sender": "FLUXWARDEN",
            "message": response_text,
            "incident_id": "INC-1042",
            "phase": agent_engine.state.current_phase,
            "mission_started": True
        }
    else:
        return {
            "sender": "FLUXWARDEN",
            "message": f"FluxWarden Autonomous SRE Agent is standby. Provide an incident objective or trigger 'RUN DEMO' to initiate adaptive recovery.",
            "mission_started": False
        }
