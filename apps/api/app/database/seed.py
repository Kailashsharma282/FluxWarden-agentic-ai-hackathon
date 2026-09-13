import asyncio
import logging
from sqlalchemy import select
from app.database.connection import AsyncSessionLocal
from app.database.migrations import run_migrations
from app.database.models import (
    SystemServiceModel,
    ScenarioModel,
    IncidentModel,
    SystemMetricModel,
    RemediationHistoryModel
)
from app.simulations.environment import sim_env
from app.api.scenarios import AVAILABLE_SCENARIOS

logger = logging.getLogger("fluxwarden.seed")

async def seed_database():
    """Seeds initial production data into PostgreSQL / database tables (Section 43)."""
    await run_migrations()

    async with AsyncSessionLocal() as session:
        # 1. Seed System Services
        for name, svc in sim_env.services.items():
            existing = await session.execute(select(SystemServiceModel).where(SystemServiceModel.name == name))
            if not existing.scalar_one_or_none():
                db_svc = SystemServiceModel(
                    name=svc.name,
                    display_name=svc.display_name,
                    type=svc.type,
                    status=svc.status,
                    health_score=svc.health_score,
                    version=svc.version,
                    cpu=svc.cpu,
                    memory=svc.memory,
                    error_rate=svc.error_rate,
                    latency_ms=svc.latency_ms,
                    request_rate=svc.request_rate,
                    dependencies=svc.dependencies,
                    configuration=svc.configuration,
                    active_target=svc.active_target
                )
                session.add(db_svc)

        # 2. Seed Scenarios
        for scen in AVAILABLE_SCENARIOS:
            existing = await session.execute(select(ScenarioModel).where(ScenarioModel.id == scen["id"]))
            if not existing.scalar_one_or_none():
                db_scen = ScenarioModel(
                    id=scen["id"],
                    title=scen["title"],
                    severity=scen["severity"],
                    description=scen["description"],
                    expected_symptoms=scen["symptoms"],
                    affected_services=scen["affected_services"],
                    adaptation_flow=scen["adaptation_flow"]
                )
                session.add(db_scen)

        # 3. Seed Primary Baseline Incident
        existing_inc = await session.execute(select(IncidentModel).where(IncidentModel.id == "INC-1042"))
        if not existing_inc.scalar_one_or_none():
            inc = IncidentModel(
                id="INC-1042",
                title="Payment API Failure & 500 Spike",
                goal="The payment API is failing. Investigate the cause and restore service without causing data loss.",
                status="UNRESOLVED",
                severity="CRITICAL",
                service="payment-api",
                summary="High error rate observed in checkout ingress. Autonomous investigation required."
            )
            session.add(inc)

        # 4. Seed Historical Remediation Memory
        hist_records = [
            {
                "id": "REM-HIST-01",
                "incident_id": "INC-HIST-881",
                "strategy_name": "Traffic failover to standby replica v40-stable",
                "scenario_id": "bad_deployment",
                "attempted_action": "route_traffic",
                "outcome": "SUCCESS",
                "adaptation_reason": "Rollback failed due to image registry hash desync",
                "confidence": 0.96,
                "duration_seconds": 38.4
            },
            {
                "id": "REM-HIST-02",
                "incident_id": "INC-HIST-742",
                "strategy_name": "Scale connection pool & reset threads",
                "scenario_id": "db_connection_exhaustion",
                "attempted_action": "scale_service",
                "outcome": "SUCCESS",
                "adaptation_reason": "Direct restart caused immediate re-saturation of connection pool",
                "confidence": 0.91,
                "duration_seconds": 24.0
            }
        ]
        for h in hist_records:
            existing_h = await session.execute(select(RemediationHistoryModel).where(RemediationHistoryModel.id == h["id"]))
            if not existing_h.scalar_one_or_none():
                db_h = RemediationHistoryModel(**h)
                session.add(db_h)

        # 5. Seed Initial Metrics Snapshot
        metric = SystemMetricModel(
            request_rate=1650,
            error_rate=0.008,
            latency_ms=45,
            cpu_usage=28,
            memory_usage=44,
            active_connections=120,
            total_services=10,
            healthy_services=10
        )
        session.add(metric)

        await session.commit()
        logger.info("Database seeding complete: 10 services, 6 scenarios, baseline incident, and historical remediation memory seeded.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(seed_database())
