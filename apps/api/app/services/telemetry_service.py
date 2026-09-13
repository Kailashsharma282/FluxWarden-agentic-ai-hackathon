import logging
from typing import Any
from app.simulations.environment import sim_env
from app.database.connection import AsyncSessionLocal
from app.database.models import SystemMetricModel
from app.database.redis_client import redis_manager

logger = logging.getLogger("fluxwarden.service.telemetry")

class TelemetryService:
    """Synchronizes simulation telemetry with Redis cache and durable metrics store."""

    async def get_live_metrics(self) -> dict[str, Any]:
        snapshot = sim_env.get_metrics_snapshot()
        # Cache snapshot in Redis for high-throughput polling
        await redis_manager.set_state("telemetry:metrics:latest", snapshot, ttl_seconds=60)
        return snapshot

    async def persist_metric_point(self):
        snapshot = sim_env.get_metrics_snapshot()
        try:
            async with AsyncSessionLocal() as session:
                metric = SystemMetricModel(
                    request_rate=snapshot["request_rate"],
                    error_rate=snapshot["error_rate"],
                    latency_ms=snapshot["latency_ms"],
                    cpu_usage=snapshot["cpu_usage"],
                    memory_usage=snapshot["memory_usage"],
                    active_connections=snapshot["active_connections"],
                    total_services=snapshot["total_services"],
                    healthy_services=snapshot["healthy_services"]
                )
                session.add(metric)
                await session.commit()
        except Exception as e:
            logger.debug(f"Metrics persist deferred: {e}")

telemetry_service = TelemetryService()
