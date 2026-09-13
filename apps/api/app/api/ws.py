import json
import logging
from typing import Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.agents.engine import agent_engine
from app.models.events import AgentEvent

logger = logging.getLogger("fluxwarden.ws")
router = APIRouter(tags=["websockets"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast_event(self, event: AgentEvent):
        dead_connections = set()
        data = event.model_dump()
        payload = json.dumps(data)
        for connection in list(self.active_connections):
            try:
                await connection.send_text(payload)
            except Exception:
                dead_connections.add(connection)
        for dead in dead_connections:
            self.active_connections.discard(dead)

ws_manager = ConnectionManager()

# Hook AgentEngine event emitter to broadcast over WebSocket
async def _on_agent_event(event: AgentEvent):
    await ws_manager.broadcast_event(event)

agent_engine.subscribe_events(_on_agent_event)

@router.websocket("/ws/events")
async def websocket_events_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # Send current state snapshot and existing events immediately on connect
        if agent_engine.state:
            await websocket.send_text(json.dumps({
                "type": "INITIAL_STATE",
                "state": agent_engine.state.model_dump(),
                "events": [e.model_dump() for e in agent_engine.events[-30:]]
            }))
        while True:
            # Keep socket alive and allow client pings
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.warning(f"WebSocket client error: {e}")
        ws_manager.disconnect(websocket)

@router.websocket("/ws/incidents/{incident_id}")
async def websocket_incident_endpoint(websocket: WebSocket, incident_id: str):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        ws_manager.disconnect(websocket)
