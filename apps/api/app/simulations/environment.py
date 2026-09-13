import copy
import time
from typing import Any, Optional
from pydantic import BaseModel, Field

class ServiceNode(BaseModel):
    name: str
    display_name: str
    type: str  # api, service, database, cache, infra
    status: str = "healthy"  # healthy, degraded, unhealthy
    health_score: int = 100
    version: str = "v41"
    cpu: int = 24
    memory: int = 38
    error_rate: float = 0.01
    latency_ms: int = 42
    request_rate: int = 1450
    dependencies: list[str] = Field(default_factory=list)
    configuration: dict[str, Any] = Field(default_factory=dict)
    active_target: bool = True  # whether receiving active traffic

class SimulationEnvironment:
    """
    Realistic simulated production environment managing 10 services:
    payment-api, auth-service, order-service, postgres, redis,
    backup-service, monitoring-service, log-service, deployment-controller, traffic-router.
    """

    def __init__(self):
        self.services: dict[str, ServiceNode] = {}
        self.active_scenario: Optional[str] = None
        self.rollback_available: bool = False  # intentionally false for Scenario A
        self.traffic_target: str = "payment-api"  # payment-api or backup-service
        self.recent_logs: list[dict[str, Any]] = []
        self.deployments: list[dict[str, Any]] = []
        self.reset_environment()

    def reset_environment(self):
        self.active_scenario = None
        self.rollback_available = False
        self.traffic_target = "payment-api"

        self.services = {
            "payment-api": ServiceNode(
                name="payment-api",
                display_name="Payment API Service",
                type="api",
                status="healthy",
                health_score=99,
                version="v41",
                cpu=28,
                memory=44,
                error_rate=0.008,
                latency_ms=45,
                request_rate=1650,
                dependencies=["auth-service", "order-service", "postgres", "redis"],
                configuration={"timeout_ms": 3000, "max_connections": 100, "cache_ttl": 300, "env": "production"},
                active_target=True
            ),
            "auth-service": ServiceNode(
                name="auth-service",
                display_name="Authentication Service",
                type="service",
                status="healthy",
                health_score=100,
                version="v18.2",
                cpu=20,
                memory=35,
                error_rate=0.001,
                latency_ms=18,
                request_rate=2100,
                dependencies=["postgres", "redis"],
                configuration={"jwt_expiry_mins": 60, "token_algorithm": "RS256"}
            ),
            "order-service": ServiceNode(
                name="order-service",
                display_name="Order Processing Service",
                type="service",
                status="healthy",
                health_score=98,
                version="v12.0",
                cpu=30,
                memory=48,
                error_rate=0.004,
                latency_ms=62,
                request_rate=980,
                dependencies=["postgres", "redis"],
                configuration={"batch_size": 50, "retry_limit": 3}
            ),
            "postgres": ServiceNode(
                name="postgres",
                display_name="PostgreSQL Primary Cluster",
                type="database",
                status="healthy",
                health_score=100,
                version="16.2",
                cpu=35,
                memory=60,
                error_rate=0.000,
                latency_ms=8,
                request_rate=4500,
                dependencies=[],
                configuration={"max_connections": 500, "active_connections": 120, "pool_size": 25}
            ),
            "redis": ServiceNode(
                name="redis",
                display_name="Redis Cache & Queue",
                type="cache",
                status="healthy",
                health_score=100,
                version="7.2.4",
                cpu=15,
                memory=28,
                error_rate=0.000,
                latency_ms=2,
                request_rate=6800,
                dependencies=[],
                configuration={"max_memory": "4GB", "eviction_policy": "volatile-lru"}
            ),
            "backup-service": ServiceNode(
                name="backup-service",
                display_name="Standby Payment Replica (Healthy Backup)",
                type="api",
                status="healthy",
                health_score=100,
                version="v40-stable",
                cpu=12,
                memory=30,
                error_rate=0.001,
                latency_ms=38,
                request_rate=0,
                dependencies=["postgres", "redis"],
                configuration={"failover_ready": True, "data_sync_delay_ms": 12},
                active_target=False
            ),
            "monitoring-service": ServiceNode(
                name="monitoring-service",
                display_name="Telemetry & Monitoring Engine",
                type="infra",
                status="healthy",
                health_score=100,
                version="v3.4",
                cpu=18,
                memory=40,
                error_rate=0.000,
                latency_ms=12,
                request_rate=500,
                dependencies=[]
            ),
            "log-service": ServiceNode(
                name="log-service",
                display_name="Log Aggregator & Indexer",
                type="infra",
                status="healthy",
                health_score=100,
                version="v2.9",
                cpu=22,
                memory=50,
                error_rate=0.000,
                latency_ms=15,
                request_rate=1200,
                dependencies=[]
            ),
            "deployment-controller": ServiceNode(
                name="deployment-controller",
                display_name="Canary & Deployment Controller",
                type="infra",
                status="healthy",
                health_score=100,
                version="v4.1",
                cpu=10,
                memory=25,
                error_rate=0.000,
                latency_ms=10,
                request_rate=50,
                dependencies=[]
            ),
            "traffic-router": ServiceNode(
                name="traffic-router",
                display_name="Global Ingress & Traffic Router",
                type="infra",
                status="healthy",
                health_score=100,
                version="v2.1",
                cpu=26,
                memory=32,
                error_rate=0.001,
                latency_ms=6,
                request_rate=1650,
                dependencies=["payment-api"],
                configuration={"active_upstream": "payment-api", "ssl_enabled": True}
            )
        }

        self.deployments = [
            {
                "id": "dep-41",
                "service": "payment-api",
                "version": "v41",
                "status": "active",
                "deployed_at": "2 hours ago",
                "author": "ci-builder",
                "commit": "a8f3b21 Fix checkout validation schema",
                "image_available": False  # Intentionally unavailable for rollback
            }
        ]

        self.recent_logs = [
            {"time": "12:00:01", "service": "payment-api", "level": "INFO", "message": "Cluster operational, handling 1650 req/s"},
            {"time": "12:00:15", "service": "auth-service", "level": "INFO", "message": "JWT token verification success rate 99.99%"},
            {"time": "12:00:30", "service": "postgres", "level": "INFO", "message": "Connection pool healthy: 120/500 active"}
        ]

    def inject_scenario(self, scenario_id: str) -> dict[str, Any]:
        self.active_scenario = scenario_id

        if scenario_id == "bad_deployment":
            # Scenario A: Bad Deployment
            self.services["payment-api"].status = "unhealthy"
            self.services["payment-api"].health_score = 22
            self.services["payment-api"].version = "v42"
            self.services["payment-api"].cpu = 72
            self.services["payment-api"].memory = 81
            self.services["payment-api"].error_rate = 0.74
            self.services["payment-api"].latency_ms = 921
            self.rollback_available = False  # Rollback MUST fail intentionally!

            self.deployments.insert(0, {
                "id": "dep-42",
                "service": "payment-api",
                "version": "v42",
                "status": "deployed",
                "deployed_at": "3 minutes ago",
                "author": "automated-pipeline",
                "commit": "c49e210 Feature: Updated Stripe v3 SDK integration",
                "image_available": True,
                "notes": "Introduced breaking signature change and unhandled schema panic"
            })

            # Mark previous image corrupted/unavailable to force agent to adapt!
            self.deployments[1]["image_available"] = False
            self.deployments[1]["error"] = "Registry image manifest corrupted: SHA256 mismatch"

            self.recent_logs.extend([
                {"time": "12:05:01", "service": "payment-api", "level": "ERROR", "message": "NullPointerReference in PaymentGateway.processTransaction() [v42]"},
                {"time": "12:05:04", "service": "payment-api", "level": "FATAL", "message": "HTTP 500 Spike: Uncaught TypeError: Cannot read property 'client_secret' of undefined"},
                {"time": "12:05:10", "service": "traffic-router", "level": "WARN", "message": "Upstream payment-api returning 74% 5xx responses; latency > 900ms"},
                {"time": "12:05:12", "service": "monitoring-service", "level": "CRITICAL", "message": "ALERT: Payment API error rate breached SLA (>70%)"}
            ])

            return {
                "scenario": "bad_deployment",
                "severity": "CRITICAL",
                "title": "Bad Production Deployment",
                "affected_services": ["payment-api", "traffic-router"],
                "symptoms": "High HTTP error rate (74%), Latency spike (921ms), Configuration mismatch, Version v42 anomaly"
            }

        elif scenario_id == "db_connection_exhaustion":
            # Scenario B: Database Connection Exhaustion
            self.services["postgres"].status = "degraded"
            self.services["postgres"].health_score = 45
            self.services["postgres"].configuration["active_connections"] = 498
            self.services["postgres"].cpu = 88
            self.services["payment-api"].status = "unhealthy"
            self.services["payment-api"].error_rate = 0.58
            self.services["payment-api"].latency_ms = 1450

            self.recent_logs.extend([
                {"time": "12:10:00", "service": "postgres", "level": "ERROR", "message": "FATAL: remaining connection slots are reserved for non-replication superuser connections"},
                {"time": "12:10:05", "service": "payment-api", "level": "ERROR", "message": "ConnectionPoolTimeout: timeout after 3000ms acquiring connection"}
            ])
            return {
                "scenario": "db_connection_exhaustion",
                "severity": "HIGH",
                "title": "Database Connection Exhaustion",
                "affected_services": ["postgres", "payment-api"],
                "symptoms": "Connection pool maxed out (498/500), API timeouts, database queries hanging"
            }

        elif scenario_id == "redis_outage":
            # Scenario C: Redis Failure
            self.services["redis"].status = "unhealthy"
            self.services["redis"].health_score = 0
            self.services["redis"].error_rate = 1.0
            self.services["payment-api"].status = "degraded"
            self.services["payment-api"].latency_ms = 480

            self.recent_logs.extend([
                {"time": "12:15:00", "service": "redis", "level": "CRITICAL", "message": "Process crashed: Out of memory during keyspace scan"},
                {"time": "12:15:02", "service": "payment-api", "level": "WARN", "message": "Redis connection refused on 6379; falling back to synchronous DB lookups"}
            ])
            return {
                "scenario": "redis_outage",
                "severity": "HIGH",
                "title": "Redis Cache Outage",
                "affected_services": ["redis", "payment-api"],
                "symptoms": "Redis offline, cache lookup failure, degraded API response time"
            }

        elif scenario_id == "memory_leak":
            # Scenario D: Memory Leak
            self.services["payment-api"].memory = 96
            self.services["payment-api"].status = "degraded"
            self.services["payment-api"].latency_ms = 850
            self.services["payment-api"].error_rate = 0.32

            self.recent_logs.extend([
                {"time": "12:20:00", "service": "payment-api", "level": "WARN", "message": "High memory consumption detected: 96% of 4GB allocated"},
                {"time": "12:20:10", "service": "payment-api", "level": "ERROR", "message": "JVM Garbage Collection paused worker threads for 420ms"}
            ])
            return {
                "scenario": "memory_leak",
                "severity": "MEDIUM",
                "title": "Payment API Memory Leak",
                "affected_services": ["payment-api"],
                "symptoms": "Memory constantly climbing to 96%, Garbage collection pauses, rising latency"
            }

        elif scenario_id == "dependency_latency":
            # Scenario E: Dependency Latency
            self.services["order-service"].latency_ms = 2400
            self.services["order-service"].status = "degraded"
            self.services["payment-api"].status = "degraded"
            self.services["payment-api"].latency_ms = 2550

            self.recent_logs.extend([
                {"time": "12:25:00", "service": "order-service", "level": "WARN", "message": "External Payment Gateway provider sandbox experiencing 2500ms response delays"}
            ])
            return {
                "scenario": "dependency_latency",
                "severity": "MEDIUM",
                "title": "Third-Party Dependency Latency",
                "affected_services": ["order-service", "payment-api"],
                "symptoms": "Upstream order-service latency 2400ms, timeouts propagating to payment API"
            }

        elif scenario_id == "network_latency":
            self.services["traffic-router"].latency_ms = 850
            self.services["traffic-router"].status = "degraded"
            return {
                "scenario": "network_latency",
                "severity": "MEDIUM",
                "title": "Ingress Network Latency",
                "affected_services": ["traffic-router"],
                "symptoms": "Packet jitter and gateway delay"
            }

        return {"scenario": "unknown", "severity": "low"}

    def get_services(self) -> list[dict[str, Any]]:
        return [node.model_dump() for node in self.services.values()]

    def get_service(self, name: str) -> Optional[dict[str, Any]]:
        if name in self.services:
            return self.services[name].model_dump()
        return None

    def get_metrics_snapshot(self) -> dict[str, Any]:
        target = self.services.get(self.traffic_target, self.services["payment-api"])
        return {
            "timestamp": time.strftime("%H:%M:%S"),
            "request_rate": target.request_rate,
            "error_rate": target.error_rate,
            "latency_ms": target.latency_ms,
            "cpu_percent": target.cpu,
            "memory_percent": target.memory,
            "db_connections": self.services["postgres"].configuration.get("active_connections", 120),
            "traffic_target": self.traffic_target,
            "active_services": len([s for s in self.services.values() if s.status == "healthy"])
        }

# Global singleton simulation instance
sim_env = SimulationEnvironment()
