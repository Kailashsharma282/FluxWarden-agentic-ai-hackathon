from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from app.simulations.environment import sim_env

router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])

AVAILABLE_SCENARIOS = [
    {
        "id": "bad_deployment",
        "title": "Bad Deployment",
        "severity": "CRITICAL",
        "description": "Deploy faulty release v42 with NullPointerReference schema mismatch in payment core.",
        "symptoms": "HTTP 500 error rate reaches 74%, Latency spikes to 921ms, Configuration mismatch.",
        "affected_services": ["payment-api", "traffic-router"],
        "adaptation_flow": "Rollback intentionally fails (registry missing v41 manifest) -> Agent replans -> Discovers standby backup -> Reroutes ingress."
    },
    {
        "id": "db_connection_exhaustion",
        "title": "Database Connection Exhaustion",
        "severity": "HIGH",
        "description": "Exhaust PostgreSQL client connection pool to 498/500 active threads.",
        "symptoms": "Application thread lockup, ConnectionPoolTimeout exceptions, degraded checkout latency.",
        "affected_services": ["postgres", "payment-api"],
        "adaptation_flow": "Scale connection pool headroom and reset leaking client threads."
    },
    {
        "id": "redis_outage",
        "title": "Redis Outage",
        "severity": "HIGH",
        "description": "Simulate abrupt Redis cache crash and eviction memory failure.",
        "symptoms": "Redis connection refused on port 6379, un-cached database thrashing.",
        "affected_services": ["redis", "payment-api"],
        "adaptation_flow": "Hot failover to standby Redis replica and warm active keyspace."
    },
    {
        "id": "memory_leak",
        "title": "Memory Leak",
        "severity": "MEDIUM",
        "description": "Inject heap memory consumption leak causing JVM worker thread lockups.",
        "symptoms": "Memory constantly increasing to 96%, Garbage collection pauses of 420ms.",
        "affected_services": ["payment-api"],
        "adaptation_flow": "Restart service container and tune runtime memory headroom."
    },
    {
        "id": "dependency_latency",
        "title": "Dependency Failure & Latency",
        "severity": "MEDIUM",
        "description": "Inject 2500ms response delays into upstream order and fraud check services.",
        "symptoms": "Timeout cascades propagating to client ingress.",
        "affected_services": ["order-service", "payment-api"],
        "adaptation_flow": "Isolate dependency with circuit breaker and activate fallback mock provider."
    },
    {
        "id": "network_latency",
        "title": "Network Latency",
        "severity": "MEDIUM",
        "description": "Simulate packet loss and ingress gateway latency jitter on traffic router.",
        "symptoms": "Traffic router latency surges to 850ms.",
        "affected_services": ["traffic-router"],
        "adaptation_flow": "Optimize ingress network routing and reload proxy configurations."
    }
]

class InjectScenarioRequest(BaseModel):
    scenario_id: str = "bad_deployment"

@router.get("")
async def list_scenarios():
    return {
        "scenarios": AVAILABLE_SCENARIOS,
        "active_scenario": sim_env.active_scenario
    }

@router.post("/inject")
async def inject_scenario(req: InjectScenarioRequest):
    result = sim_env.inject_scenario(req.scenario_id)
    return {
        "status": "injected",
        "scenario": req.scenario_id,
        "details": result,
        "metrics": sim_env.get_metrics_snapshot()
    }

@router.post("/reset")
async def reset_scenarios():
    sim_env.reset_environment()
    return {
        "status": "reset_complete",
        "active_scenario": None,
        "metrics": sim_env.get_metrics_snapshot(),
        "services": sim_env.get_services()
    }
