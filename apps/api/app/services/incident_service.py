import logging
from datetime import datetime, timezone
from typing import Any, Optional
from sqlalchemy import select, update
from app.database.connection import AsyncSessionLocal
from app.database.models import IncidentModel, IncidentEventModel, AgentRunModel
from app.database.redis_client import redis_manager
from app.models.state import AgentState
from app.models.events import AgentEvent

logger = logging.getLogger("fluxwarden.service.incident")

class IncidentService:
    """Manages durable persistence to PostgreSQL (Section 43) and Redis caching (Section 44)."""

    async def save_incident(self, incident_id: str, title: str, goal: str, severity: str = "HIGH") -> dict[str, Any]:
        record = {
            "id": incident_id,
            "title": title,
            "goal": goal,
            "status": "UNRESOLVED",
            "severity": severity,
            "service": "payment-api",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        # Update Redis cache
        await redis_manager.set_state(f"incident:{incident_id}", record)

        # Persist to database
        try:
            async with AsyncSessionLocal() as session:
                existing = await session.execute(select(IncidentModel).where(IncidentModel.id == incident_id))
                if not existing.scalar_one_or_none():
                    inc = IncidentModel(
                        id=incident_id,
                        title=title,
                        goal=goal,
                        status="UNRESOLVED",
                        severity=severity,
                        service="payment-api"
                    )
                    session.add(inc)
                    await session.commit()
        except Exception as e:
            logger.debug(f"Database persist for incident {incident_id} deferred: {e}")
        return record

    async def record_event(self, event: AgentEvent):
        # Broadcast over Redis channel for WebSocket coordination (Section 44)
        await redis_manager.publish_event("fluxwarden:events", event.model_dump())

        # Persist durable event
        try:
            async with AsyncSessionLocal() as session:
                ev_model = IncidentEventModel(
                    id=event.id,
                    incident_id=event.incident_id,
                    type=event.type,
                    tool=event.tool,
                    summary=event.summary,
                    severity=event.severity,
                    details=event.details
                )
                session.add(ev_model)
                await session.commit()
        except Exception as e:
            logger.debug(f"Database persist for event {event.id} deferred: {e}")

    async def update_resolution(self, incident_id: str, status: str, final_report: Optional[dict[str, Any]] = None):
        await redis_manager.set_state(f"incident:{incident_id}:status", status)
        try:
            async with AsyncSessionLocal() as session:
                stmt = (
                    update(IncidentModel)
                    .where(IncidentModel.id == incident_id)
                    .values(
                        status=status,
                        final_report=final_report,
                        resolved_at=datetime.now(timezone.utc) if status == "RESOLVED" else None
                    )
                )
                await session.execute(stmt)
                await session.commit()
        except Exception as e:
            logger.debug(f"Database update for incident resolution deferred: {e}")

incident_service = IncidentService()
