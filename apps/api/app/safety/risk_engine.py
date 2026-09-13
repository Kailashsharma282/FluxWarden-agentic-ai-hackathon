from typing import Any, Optional
from pydantic import BaseModel

class RiskAssessment(BaseModel):
    tool: str
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    requires_approval: bool
    impact_summary: str
    safety_notes: str

class RiskEngine:
    """
    Evaluates action risk and enforces safety guardrails.
    Critical/destructive operations must never execute automatically.
    High-risk actions require human-in-the-loop approval.
    """
    TOOL_RISK_MAP = {
        # Low risk
        "get_service_status": "LOW",
        "get_service_health": "LOW",
        "get_recent_logs": "LOW",
        "search_logs": "LOW",
        "get_metrics": "LOW",
        "get_error_rate": "LOW",
        "get_latency": "LOW",
        "get_cpu_usage": "LOW",
        "get_memory_usage": "LOW",
        "get_database_health": "LOW",
        "get_redis_health": "LOW",
        "get_dependency_status": "LOW",
        "get_recent_deployments": "LOW",
        "get_current_configuration": "LOW",
        "inspect_network": "LOW",
        "get_backup_status": "LOW",
        "get_traffic_distribution": "LOW",
        "restart_service": "LOW",
        "clear_cache": "LOW",
        "create_incident_report": "LOW",
        "close_incident": "LOW",
        "run_health_check": "LOW",
        "run_smoke_test": "LOW",
        "run_payment_test": "LOW",
        "check_error_rate": "LOW",
        "check_latency": "LOW",
        "check_dependency_health": "LOW",
        "verify_database_integrity": "LOW",
        "verify_traffic_distribution": "LOW",
        "verify_service_recovery": "LOW",

        # Medium risk
        "route_traffic": "MEDIUM",
        "scale_service": "MEDIUM",
        "restore_configuration": "MEDIUM",
        "rollback_deployment": "MEDIUM",
        "disable_dependency": "MEDIUM",
        "escalate_incident": "MEDIUM",

        # High risk
        "failover_service": "HIGH",
        "restore_backup": "HIGH",
        "request_human_approval": "HIGH",

        # Critical
        "delete_data": "CRITICAL",
        "drop_database": "CRITICAL"
    }

    def assess_risk(self, tool_name: str, params: Optional[dict[str, Any]] = None) -> RiskAssessment:
        risk = self.TOOL_RISK_MAP.get(tool_name, "MEDIUM")
        requires_approval = (risk in ["HIGH", "CRITICAL"])

        impacts = {
            "LOW": "Read-only inspection or non-disruptive transient reset.",
            "MEDIUM": "Modifies network routing or pod allocation within standard operational parameters.",
            "HIGH": "Changes persistent state or triggers major service topology failover.",
            "CRITICAL": "Potentially destructive or irreversible operation."
        }

        safety = {
            "LOW": "Safe to execute autonomously.",
            "MEDIUM": "Monitored autonomous execution with rollback telemetry.",
            "HIGH": "Requires explicit operator verification before executing.",
            "CRITICAL": "Strictly blocked from autonomous execution. Operator intervention mandatory."
        }

        return RiskAssessment(
            tool=tool_name,
            risk_level=risk,
            requires_approval=requires_approval,
            impact_summary=impacts.get(risk, "Standard operation"),
            safety_notes=safety.get(risk, "Standard safety checks")
        )

risk_engine = RiskEngine()
