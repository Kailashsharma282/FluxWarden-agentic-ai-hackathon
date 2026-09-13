from typing import Any
from app.tools.registry import tool_registry

class VerificationResult:
    def __init__(self, passed: bool, resolution_status: str, checks: dict[str, Any], message: str):
        self.passed = passed
        self.resolution_status = resolution_status
        self.checks = checks
        self.message = message

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "resolution_status": self.resolution_status,
            "checks": self.checks,
            "message": self.message
        }

class VerificationEngine:
    """
    Mandatory Verification Engine (Section 20).
    An action returning {"success": true} does NOT automatically resolve the incident.
    Must independently run the full multi-check verification suite:
    - health check
    - smoke test
    - error rate verification
    - latency verification
    - dependency verification
    - database integrity verification
    """

    async def verify_incident(self, incident_id: str, target_service: str = "payment-api") -> VerificationResult:
        checks: dict[str, Any] = {}

        # 1. Health check
        res_health = await tool_registry.execute("run_health_check", {"service_name": None})
        checks["health_check"] = {
            "passed": res_health.success,
            "data": res_health.data,
            "title": "Service Health & Liveness Probe"
        }

        # 2. Smoke test
        res_smoke = await tool_registry.execute("run_smoke_test", {"target": None})
        checks["smoke_test"] = {
            "passed": res_smoke.success,
            "data": res_smoke.data,
            "title": "Synthetic API Surface Smoke Test"
        }

        # 3. Error rate verification
        res_err = await tool_registry.execute("check_error_rate", {"service_name": None})
        checks["error_rate_verification"] = {
            "passed": res_err.success,
            "data": res_err.data,
            "title": "Error Rate SLA Check (<5%)"
        }

        # 4. Latency verification
        res_lat = await tool_registry.execute("check_latency", {"service_name": None})
        checks["latency_verification"] = {
            "passed": res_lat.success,
            "data": res_lat.data,
            "title": "Latency p95 SLA Check (<200ms)"
        }

        # 5. Dependency verification
        res_dep = await tool_registry.execute("check_dependency_health", {})
        checks["dependency_verification"] = {
            "passed": res_dep.success,
            "data": res_dep.data,
            "title": "Upstream/Downstream Dependency Verification"
        }

        # 6. Database integrity verification
        res_db = await tool_registry.execute("verify_database_integrity", {})
        checks["database_integrity"] = {
            "passed": res_db.success,
            "data": res_db.data,
            "title": "ACID Database Transaction & Connection Pool Integrity"
        }

        all_passed = all(c["passed"] for c in checks.values())

        if all_passed:
            return VerificationResult(
                passed=True,
                resolution_status="RESOLVED",
                checks=checks,
                message="All 6 independent verification probes passed successfully. Target service verified operational."
            )
        else:
            failed_probes = [k for k, v in checks.items() if not v["passed"]]
            return VerificationResult(
                passed=False,
                resolution_status="STILL_UNHEALTHY",
                checks=checks,
                message=f"Verification failed on probes: {', '.join(failed_probes)}. Target is still unhealthy."
            )

verification_engine = VerificationEngine()
