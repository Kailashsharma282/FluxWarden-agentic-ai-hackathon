import time
from datetime import datetime, timezone
from typing import Any, Callable, Coroutine, Optional
from app.simulations.environment import sim_env
from app.tools.base import ToolDefinition, ToolResult

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}
        self._handlers: dict[str, Callable[..., Coroutine[Any, Any, ToolResult]]] = {}
        self._register_all_tools()

    def register(
        self,
        name: str,
        description: str,
        category: str,
        risk_level: str,
        input_schema: dict[str, Any],
        output_schema: dict[str, Any],
        handler: Callable[..., Coroutine[Any, Any, ToolResult]],
        timeout_seconds: int = 10,
        retry_policy: Optional[dict[str, Any]] = None
    ):
        tool_def = ToolDefinition(
            name=name,
            description=description,
            category=category,
            risk_level=risk_level,
            input_schema=input_schema,
            output_schema=output_schema,
            timeout_seconds=timeout_seconds,
            retry_policy=retry_policy or {"max_retries": 2, "backoff_ms": 500}
        )
        self._tools[name] = tool_def
        self._handlers[name] = handler

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        return self._tools.get(name)

    def list_tools(self) -> list[dict[str, Any]]:
        return [t.model_dump() for t in self._tools.values()]

    async def execute(self, name: str, params: dict[str, Any]) -> ToolResult:
        if name not in self._handlers:
            return ToolResult(
                tool=name,
                success=False,
                data=None,
                error=f"Unknown tool '{name}' in Tool Registry.",
                timestamp=datetime.now(timezone.utc).isoformat()
            )

        start_time = time.time()
        try:
            handler = self._handlers[name]
            result = await handler(**params)
            result.execution_time_ms = int((time.time() - start_time) * 1000)
            result.timestamp = datetime.now(timezone.utc).isoformat()
            return result
        except Exception as e:
            return ToolResult(
                tool=name,
                success=False,
                data=None,
                error=f"Execution error in {name}: {str(e)}",
                execution_time_ms=int((time.time() - start_time) * 1000),
                timestamp=datetime.now(timezone.utc).isoformat()
            )

    def _register_all_tools(self):
        # -------------------------------------------------------------
        # 10. DIAGNOSTIC TOOLS (17 tools)
        # -------------------------------------------------------------
        async def handle_get_service_status(service_name: str = "payment-api") -> ToolResult:
            svc = sim_env.get_service(service_name)
            if not svc:
                return ToolResult(tool="get_service_status", success=False, data=None, error=f"Service {service_name} not found")
            return ToolResult(tool="get_service_status", success=True, data={"service": service_name, "status": svc["status"], "health_score": svc["health_score"], "version": svc["version"]})

        async def handle_get_service_health(service_name: str = "payment-api") -> ToolResult:
            svc = sim_env.get_service(service_name)
            if not svc:
                return ToolResult(tool="get_service_health", success=False, data=None, error=f"Service {service_name} not found")
            return ToolResult(tool="get_service_health", success=True, data={
                "service": service_name,
                "health_score": svc["health_score"],
                "status": svc["status"],
                "error_rate": svc["error_rate"],
                "latency_ms": svc["latency_ms"]
            })

        async def handle_get_recent_logs(service_name: str = "payment-api", limit: int = 10) -> ToolResult:
            logs = [log for log in sim_env.recent_logs if log.get("service") == service_name or service_name == "all"]
            return ToolResult(tool="get_recent_logs", success=True, data={"logs": logs[-limit:], "count": len(logs[-limit:])})

        async def handle_search_logs(query: str = "error") -> ToolResult:
            matched = [l for l in sim_env.recent_logs if query.lower() in l.get("message", "").lower() or query.lower() in l.get("level", "").lower()]
            return ToolResult(tool="search_logs", success=True, data={"query": query, "matches": matched})

        async def handle_get_metrics(service_name: str = "payment-api") -> ToolResult:
            svc = sim_env.get_service(service_name)
            if not svc:
                return ToolResult(tool="get_metrics", success=False, data=None, error=f"Service {service_name} not found")
            return ToolResult(tool="get_metrics", success=True, data={
                "service": service_name,
                "cpu": svc["cpu"],
                "memory": svc["memory"],
                "error_rate": svc["error_rate"],
                "latency_ms": svc["latency_ms"],
                "request_rate": svc["request_rate"]
            })

        async def handle_get_error_rate(service_name: str = "payment-api") -> ToolResult:
            svc = sim_env.get_service(service_name)
            return ToolResult(tool="get_error_rate", success=True, data={"service": service_name, "error_rate": svc["error_rate"] if svc else 0.0})

        async def handle_get_latency(service_name: str = "payment-api") -> ToolResult:
            svc = sim_env.get_service(service_name)
            return ToolResult(tool="get_latency", success=True, data={"service": service_name, "latency_ms": svc["latency_ms"] if svc else 0})

        async def handle_get_cpu_usage(service_name: str = "payment-api") -> ToolResult:
            svc = sim_env.get_service(service_name)
            return ToolResult(tool="get_cpu_usage", success=True, data={"service": service_name, "cpu_percent": svc["cpu"] if svc else 0})

        async def handle_get_memory_usage(service_name: str = "payment-api") -> ToolResult:
            svc = sim_env.get_service(service_name)
            return ToolResult(tool="get_memory_usage", success=True, data={"service": service_name, "memory_percent": svc["memory"] if svc else 0})

        async def handle_get_database_health() -> ToolResult:
            db = sim_env.get_service("postgres")
            return ToolResult(tool="get_database_health", success=True, data={
                "service": "postgres",
                "status": db["status"],
                "connections": db["configuration"].get("active_connections", 120),
                "max_connections": db["configuration"].get("max_connections", 500)
            })

        async def handle_get_redis_health() -> ToolResult:
            red = sim_env.get_service("redis")
            return ToolResult(tool="get_redis_health", success=True, data={
                "service": "redis",
                "status": red["status"],
                "health_score": red["health_score"],
                "error_rate": red["error_rate"]
            })

        async def handle_get_dependency_status(service_name: str = "payment-api") -> ToolResult:
            svc = sim_env.get_service(service_name)
            deps = svc.get("dependencies", []) if svc else []
            dep_statuses = {dep: sim_env.get_service(dep)["status"] for dep in deps if sim_env.get_service(dep)}
            return ToolResult(tool="get_dependency_status", success=True, data={"service": service_name, "dependencies": dep_statuses})

        async def handle_get_recent_deployments(service_name: str = "payment-api") -> ToolResult:
            deps = [d for d in sim_env.deployments if d.get("service") == service_name]
            return ToolResult(tool="get_recent_deployments", success=True, data={"service": service_name, "deployments": deps})

        async def handle_get_current_configuration(service_name: str = "payment-api") -> ToolResult:
            svc = sim_env.get_service(service_name)
            return ToolResult(tool="get_current_configuration", success=True, data={"service": service_name, "configuration": svc.get("configuration", {}) if svc else {}})

        async def handle_inspect_network() -> ToolResult:
            router = sim_env.get_service("traffic-router")
            return ToolResult(tool="inspect_network", success=True, data={
                "gateway": "traffic-router",
                "status": router["status"],
                "latency_ms": router["latency_ms"],
                "target": sim_env.traffic_target
            })

        async def handle_get_backup_status() -> ToolResult:
            backup = sim_env.get_service("backup-service")
            return ToolResult(tool="get_backup_status", success=True, data={
                "service": "backup-service",
                "status": backup["status"],
                "health_score": backup["health_score"],
                "version": backup["version"],
                "ready": backup["configuration"].get("failover_ready", True),
                "active_traffic": backup.get("active_target", False)
            })

        async def handle_get_traffic_distribution() -> ToolResult:
            return ToolResult(tool="get_traffic_distribution", success=True, data={
                "active_target": sim_env.traffic_target,
                "distribution": {sim_env.traffic_target: 100}
            })

        # Register Diagnostics
        diag_tools = [
            ("get_service_status", "Check basic operational status and health score of a service", handle_get_service_status),
            ("get_service_health", "Retrieve comprehensive telemetry and health metrics for a service", handle_get_service_health),
            ("get_recent_logs", "Retrieve the latest stderr/stdout logs for a specific service", handle_get_recent_logs),
            ("search_logs", "Full-text search through recent infrastructure log entries", handle_search_logs),
            ("get_metrics", "Query resource usage (CPU, RAM, latency, errors) for a service", handle_get_metrics),
            ("get_error_rate", "Extract current HTTP 5xx / 4xx error rate ratio", handle_get_error_rate),
            ("get_latency", "Measure round-trip p95/p99 latency in milliseconds", handle_get_latency),
            ("get_cpu_usage", "Inspect percentage of CPU allocated to container instance", handle_get_cpu_usage),
            ("get_memory_usage", "Inspect percentage of memory consumption", handle_get_memory_usage),
            ("get_database_health", "Check PostgreSQL connection pool and query engine health", handle_get_database_health),
            ("get_redis_health", "Verify Redis cache connectivity and eviction status", handle_get_redis_health),
            ("get_dependency_status", "Inspect upstream and downstream dependencies for a given service", handle_get_dependency_status),
            ("get_recent_deployments", "Fetch recent CI/CD deployments, commit hashes, and container images", handle_get_recent_deployments),
            ("get_current_configuration", "Inspect active environment configuration and runtime variables", handle_get_current_configuration),
            ("inspect_network", "Examine gateway routing, ingress status, and packet health", handle_inspect_network),
            ("get_backup_status", "Check readiness and data synchronization of the backup service", handle_get_backup_status),
            ("get_traffic_distribution", "Inspect current load balancer traffic percentage distribution", handle_get_traffic_distribution),
        ]
        for name, desc, handler in diag_tools:
            self.register(
                name=name,
                description=desc,
                category="diagnostic",
                risk_level="LOW",
                input_schema={"type": "object", "properties": {"service_name": {"type": "string"}}},
                output_schema={"type": "object"},
                handler=handler
            )

        # -------------------------------------------------------------
        # 11. REMEDIATION TOOLS (9 tools)
        # -------------------------------------------------------------
        async def handle_restart_service(service_name: str = "payment-api") -> ToolResult:
            if service_name in sim_env.services:
                svc = sim_env.services[service_name]
                if sim_env.active_scenario == "memory_leak":
                    svc.memory = 42
                    svc.status = "healthy"
                    svc.error_rate = 0.01
                    svc.latency_ms = 45
                    return ToolResult(tool="restart_service", success=True, data={"service": service_name, "message": "Service restarted, memory leak flushed."})
                elif sim_env.active_scenario == "bad_deployment":
                    # Restarting bad deployment code still fails!
                    return ToolResult(tool="restart_service", success=True, data={"service": service_name, "message": "Service container restarted, but startup validation failed with v42 fatal exception."})
                svc.status = "healthy"
                return ToolResult(tool="restart_service", success=True, data={"service": service_name, "message": "Service restarted successfully."})
            return ToolResult(tool="restart_service", success=False, data=None, error="Service not found")

        async def handle_rollback_deployment(service_name: str = "payment-api") -> ToolResult:
            # SECTION 3 & 4 DEMO REQUIREMENT:
            # The failed rollback is intentional! This is the central demonstration of adaptation!
            if sim_env.active_scenario == "bad_deployment" and not sim_env.rollback_available:
                return ToolResult(
                    tool="rollback_deployment",
                    success=False,
                    data=None,
                    error="Rollback failed: Previous image v41 manifest missing/corrupted in registry (SHA256 mismatch). Rollback aborted."
                )
            if service_name in sim_env.services:
                sim_env.services[service_name].version = "v41"
                sim_env.services[service_name].status = "healthy"
                sim_env.services[service_name].error_rate = 0.01
                return ToolResult(tool="rollback_deployment", success=True, data={"service": service_name, "version": "v41", "message": "Rollback successful"})
            return ToolResult(tool="rollback_deployment", success=False, data=None, error="Service not found")

        async def handle_restore_configuration(service_name: str = "payment-api") -> ToolResult:
            if service_name in sim_env.services:
                sim_env.services[service_name].configuration = {"timeout_ms": 3000, "max_connections": 100, "cache_ttl": 300}
                return ToolResult(tool="restore_configuration", success=True, data={"service": service_name, "message": "Configuration restored to default stable baseline"})
            return ToolResult(tool="restore_configuration", success=False, data=None, error="Service not found")

        async def handle_route_traffic(target_service: str = "backup-service") -> ToolResult:
            if target_service not in sim_env.services:
                return ToolResult(tool="route_traffic", success=False, data=None, error=f"Target {target_service} not in topology")
            sim_env.traffic_target = target_service
            # Update target active flags
            for sname, s in sim_env.services.items():
                s.active_target = (sname == target_service)
            # Update traffic router upstream
            sim_env.services["traffic-router"].configuration["active_upstream"] = target_service
            return ToolResult(tool="route_traffic", success=True, data={
                "traffic_target": target_service,
                "message": f"Global traffic ingress successfully rerouted to {target_service}."
            })

        async def handle_scale_service(service_name: str = "payment-api", replicas: int = 3) -> ToolResult:
            if service_name in sim_env.services:
                if sim_env.active_scenario == "db_connection_exhaustion":
                    sim_env.services["postgres"].configuration["active_connections"] = 150
                    sim_env.services["postgres"].status = "healthy"
                    sim_env.services["payment-api"].error_rate = 0.01
                    sim_env.services["payment-api"].status = "healthy"
                return ToolResult(tool="scale_service", success=True, data={"service": service_name, "replicas": replicas, "message": f"Scaled {service_name} to {replicas} replicas."})
            return ToolResult(tool="scale_service", success=False, data=None, error="Service not found")

        async def handle_clear_cache(cache_name: str = "redis") -> ToolResult:
            if cache_name in sim_env.services:
                return ToolResult(tool="clear_cache", success=True, data={"cache": cache_name, "message": "Cache flushed and warmed."})
            return ToolResult(tool="clear_cache", success=False, data=None, error="Cache not found")

        async def handle_failover_service(service_name: str = "redis") -> ToolResult:
            if service_name == "redis":
                sim_env.services["redis"].status = "healthy"
                sim_env.services["redis"].health_score = 100
                sim_env.services["redis"].error_rate = 0.00
                sim_env.services["payment-api"].status = "healthy"
                sim_env.services["payment-api"].latency_ms = 45
                return ToolResult(tool="failover_service", success=True, data={"service": "redis", "message": "Redis failed over to standby replica. Cache operational."})
            return ToolResult(tool="failover_service", success=True, data={"service": service_name, "message": f"Failover triggered for {service_name}"})

        async def handle_restore_backup(backup_id: str = "backup-daily-01") -> ToolResult:
            return ToolResult(tool="restore_backup", success=True, data={"backup_id": backup_id, "status": "restored", "message": "Data state restored from snapshot"})

        async def handle_disable_dependency(dependency_name: str = "order-service") -> ToolResult:
            if dependency_name in sim_env.services:
                sim_env.services[dependency_name].status = "disabled"
                return ToolResult(tool="disable_dependency", success=True, data={"dependency": dependency_name, "message": f"Dependency {dependency_name} isolated with circuit breaker."})
            return ToolResult(tool="disable_dependency", success=False, data=None, error="Dependency not found")

        # Register Remediations with defined risk levels
        self.register("restart_service", "Restart an instance or container", "remediation", "LOW", {"type": "object", "properties": {"service_name": {"type": "string"}}}, {"type": "object"}, handle_restart_service)
        self.register("rollback_deployment", "Rollback to the previous deployment version in registry", "remediation", "MEDIUM", {"type": "object", "properties": {"service_name": {"type": "string"}}}, {"type": "object"}, handle_rollback_deployment)
        self.register("restore_configuration", "Revert service configuration parameters to standard stable baseline", "remediation", "MEDIUM", {"type": "object", "properties": {"service_name": {"type": "string"}}}, {"type": "object"}, handle_restore_configuration)
        self.register("route_traffic", "Reroute ingress traffic to an alternate or standby service instance", "remediation", "MEDIUM", {"type": "object", "properties": {"target_service": {"type": "string"}}}, {"type": "object"}, handle_route_traffic)
        self.register("scale_service", "Dynamically scale service pod replica count", "remediation", "MEDIUM", {"type": "object", "properties": {"service_name": {"type": "string"}, "replicas": {"type": "integer"}}}, {"type": "object"}, handle_scale_service)
        self.register("clear_cache", "Flush corrupted or stale keys from the cache layer", "remediation", "LOW", {"type": "object", "properties": {"cache_name": {"type": "string"}}}, {"type": "object"}, handle_clear_cache)
        self.register("failover_service", "Promote replica to primary or failover service instance", "remediation", "HIGH", {"type": "object", "properties": {"service_name": {"type": "string"}}}, {"type": "object"}, handle_failover_service)
        self.register("restore_backup", "Restore state from persistent snapshot (Destructive)", "remediation", "HIGH", {"type": "object", "properties": {"backup_id": {"type": "string"}}}, {"type": "object"}, handle_restore_backup)
        self.register("disable_dependency", "Isolate flaky dependency via circuit breaker", "remediation", "MEDIUM", {"type": "object", "properties": {"dependency_name": {"type": "string"}}}, {"type": "object"}, handle_disable_dependency)

        # -------------------------------------------------------------
        # 12. VERIFICATION TOOLS (9 tools)
        # -------------------------------------------------------------
        async def handle_run_health_check(service_name: Optional[str] = None) -> ToolResult:
            target = service_name or sim_env.traffic_target
            svc = sim_env.get_service(target)
            passed = svc["status"] == "healthy" and svc["health_score"] >= 90
            return ToolResult(tool="run_health_check", success=passed, data={"target": target, "status": svc["status"], "passed": passed})

        async def handle_run_smoke_test(target: Optional[str] = None) -> ToolResult:
            actual = target or sim_env.traffic_target
            svc = sim_env.get_service(actual)
            passed = svc["error_rate"] < 0.05
            return ToolResult(tool="run_smoke_test", success=passed, data={"target": actual, "synthetic_transactions_passed": 50 if passed else 12, "passed": passed})

        async def handle_run_payment_test() -> ToolResult:
            actual = sim_env.traffic_target
            svc = sim_env.get_service(actual)
            passed = svc["error_rate"] < 0.05 and svc["status"] == "healthy"
            return ToolResult(tool="run_payment_test", success=passed, data={"endpoint": f"/v1/charges via {actual}", "charge_success": passed, "latency_ms": svc["latency_ms"]})

        async def handle_check_error_rate(service_name: Optional[str] = None) -> ToolResult:
            actual = service_name or sim_env.traffic_target
            svc = sim_env.get_service(actual)
            passed = svc["error_rate"] < 0.05
            return ToolResult(tool="check_error_rate", success=passed, data={"target": actual, "error_rate": svc["error_rate"], "threshold": 0.05, "passed": passed})

        async def handle_check_latency(service_name: Optional[str] = None) -> ToolResult:
            actual = service_name or sim_env.traffic_target
            svc = sim_env.get_service(actual)
            passed = svc["latency_ms"] < 200
            return ToolResult(tool="check_latency", success=passed, data={"target": actual, "latency_ms": svc["latency_ms"], "threshold_ms": 200, "passed": passed})

        async def handle_check_dependency_health() -> ToolResult:
            target = sim_env.traffic_target
            svc = sim_env.get_service(target)
            deps = svc.get("dependencies", [])
            all_healthy = all(sim_env.get_service(d)["status"] != "unhealthy" for d in deps if sim_env.get_service(d))
            return ToolResult(tool="check_dependency_health", success=all_healthy, data={"target": target, "dependencies_checked": deps, "passed": all_healthy})

        async def handle_verify_database_integrity() -> ToolResult:
            db = sim_env.get_service("postgres")
            passed = db["status"] != "unhealthy" and db["configuration"].get("active_connections", 120) < 450
            return ToolResult(tool="verify_database_integrity", success=passed, data={"db_status": db["status"], "acid_transactions": "verified", "passed": passed})

        async def handle_verify_traffic_distribution() -> ToolResult:
            target = sim_env.traffic_target
            svc = sim_env.get_service(target)
            passed = svc["status"] == "healthy"
            return ToolResult(tool="verify_traffic_distribution", success=passed, data={"active_target": target, "passed": passed})

        async def handle_verify_service_recovery() -> ToolResult:
            target = sim_env.traffic_target
            svc = sim_env.get_service(target)
            passed = svc["status"] == "healthy" and svc["error_rate"] < 0.05
            return ToolResult(tool="verify_service_recovery", success=passed, data={"target": target, "recovered": passed})

        # Register Verification Tools
        verif_tools = [
            ("run_health_check", "Run deep HTTP and system health check", handle_run_health_check),
            ("run_smoke_test", "Execute synthetic test suite across API surface", handle_smoke_test := handle_run_smoke_test),
            ("run_payment_test", "Execute mock end-to-end checkout transactions", handle_run_payment_test),
            ("check_error_rate", "Verify error rate is beneath the 5% SLA threshold", handle_check_error_rate),
            ("check_latency", "Verify response latency is beneath the 200ms threshold", handle_check_latency),
            ("check_dependency_health", "Verify all connected dependencies are responsive", handle_check_dependency_health),
            ("verify_database_integrity", "Verify database integrity and connection availability", handle_verify_database_integrity),
            ("verify_traffic_distribution", "Confirm traffic router is correctly directing load", handle_verify_traffic_distribution),
            ("verify_service_recovery", "Comprehensive multi-check verification confirmation", handle_verify_service_recovery),
        ]
        for name, desc, handler in verif_tools:
            self.register(name=name, description=desc, category="verification", risk_level="LOW", input_schema={"type": "object"}, output_schema={"type": "object"}, handler=handler)

        # -------------------------------------------------------------
        # 13. SAFETY TOOLS (4 tools)
        # -------------------------------------------------------------
        async def handle_request_human_approval(action: str, impact: str, reason: str, safety: str) -> ToolResult:
            return ToolResult(tool="request_human_approval", success=True, data={
                "action": action,
                "impact": impact,
                "reason": reason,
                "safety": safety,
                "status": "pending_human_review"
            })

        async def handle_create_incident_report(incident_id: str) -> ToolResult:
            return ToolResult(tool="create_incident_report", success=True, data={
                "incident_id": incident_id,
                "status": "generated",
                "team": "kailashsharma8",
                "lead": "Pochiraju Kailash Ram Markandeya Sharma",
                "hackathon": "Tech Zephyr 4.0 | IIT Bhubaneswar"
            })

        async def handle_escalate_incident(incident_id: str, reason: str) -> ToolResult:
            return ToolResult(tool="escalate_incident", success=True, data={"incident_id": incident_id, "escalation": "on_call_page_dispatched", "reason": reason})

        async def handle_close_incident(incident_id: str, resolution_summary: str) -> ToolResult:
            return ToolResult(tool="close_incident", success=True, data={"incident_id": incident_id, "status": "CLOSED", "summary": resolution_summary})

        self.register("request_human_approval", "Pause autonomous execution and prompt human operator for confirmation", "safety", "HIGH", {"type": "object"}, {"type": "object"}, handle_request_human_approval)
        self.register("create_incident_report", "Compile incident forensic summary and export artifact", "safety", "LOW", {"type": "object"}, {"type": "object"}, handle_create_incident_report)
        self.register("escalate_incident", "Escalate incident to human engineering on-call responders", "safety", "MEDIUM", {"type": "object"}, {"type": "object"}, handle_escalate_incident)
        self.register("close_incident", "Formally mark incident resolved and archive state", "safety", "LOW", {"type": "object"}, {"type": "object"}, handle_close_incident)

# Global singleton tool registry
tool_registry = ToolRegistry()
