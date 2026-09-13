import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    Text,
    DateTime,
    JSON,
    ForeignKey
)
from app.database.connection import Base

class IncidentModel(Base):
    """Table 1: incidents (Section 43)"""
    __tablename__ = "incidents"

    id = Column(String(64), primary_key=True, default=lambda: f"INC-{uuid.uuid4().hex[:6].upper()}")
    title = Column(String(255), nullable=False)
    goal = Column(Text, nullable=False)
    status = Column(String(50), default="UNRESOLVED")  # UNRESOLVED, INVESTIGATING, RESOLVED, STILL_UNHEALTHY, ESCALATED
    severity = Column(String(20), default="HIGH")  # LOW, MEDIUM, HIGH, CRITICAL
    service = Column(String(64), default="payment-api")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime, nullable=True)
    summary = Column(Text, nullable=True)
    final_report = Column(JSON, nullable=True)

class IncidentEventModel(Base):
    """Table 2: incident_events (Section 43)"""
    __tablename__ = "incident_events"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String(64), ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    type = Column(String(64), nullable=False)  # GOAL_ACCEPTED, TOOL_SELECTED, ACTION_FAILED, etc.
    tool = Column(String(64), nullable=True)
    summary = Column(Text, nullable=False)
    severity = Column(String(20), default="info")
    details = Column(JSON, nullable=True)

class AgentRunModel(Base):
    """Table 3: agent_runs (Section 43)"""
    __tablename__ = "agent_runs"

    id = Column(String(64), primary_key=True, default=lambda: f"RUN-{uuid.uuid4().hex[:8]}")
    incident_id = Column(String(64), ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    provider = Column(String(32), default="mock")  # mock, openai, gemini, anthropic
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime, nullable=True)
    step_count = Column(Integer, default=0)
    replan_count = Column(Integer, default=0)
    status = Column(String(32), default="RUNNING")  # RUNNING, COMPLETED, FAILED, ESCALATED
    state_snapshot = Column(JSON, nullable=True)

class ToolExecutionModel(Base):
    """Table 4: tool_executions (Section 43)"""
    __tablename__ = "tool_executions"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String(64), index=True, nullable=True)
    run_id = Column(String(64), index=True, nullable=True)
    tool_name = Column(String(64), nullable=False)
    category = Column(String(32), default="diagnostic")
    risk_level = Column(String(20), default="LOW")
    parameters = Column(JSON, nullable=True)
    result_data = Column(JSON, nullable=True)
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    execution_time_ms = Column(Integer, default=0)
    executed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class SystemServiceModel(Base):
    """Table 5: system_services (Section 43)"""
    __tablename__ = "system_services"

    name = Column(String(64), primary_key=True)
    display_name = Column(String(128), nullable=False)
    type = Column(String(32), default="service")
    status = Column(String(32), default="healthy")  # healthy, degraded, unhealthy
    health_score = Column(Integer, default=100)
    version = Column(String(32), default="v41")
    cpu = Column(Integer, default=20)
    memory = Column(Integer, default=40)
    error_rate = Column(Float, default=0.01)
    latency_ms = Column(Integer, default=40)
    request_rate = Column(Integer, default=1000)
    dependencies = Column(JSON, nullable=True)
    configuration = Column(JSON, nullable=True)
    active_target = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class SystemMetricModel(Base):
    """Table 6: system_metrics (Section 43)"""
    __tablename__ = "system_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    request_rate = Column(Integer, default=1650)
    error_rate = Column(Float, default=0.008)
    latency_ms = Column(Integer, default=45)
    cpu_usage = Column(Integer, default=28)
    memory_usage = Column(Integer, default=44)
    active_connections = Column(Integer, default=120)
    total_services = Column(Integer, default=10)
    healthy_services = Column(Integer, default=10)

class ScenarioModel(Base):
    """Table 7: scenarios (Section 43)"""
    __tablename__ = "scenarios"

    id = Column(String(64), primary_key=True)
    title = Column(String(128), nullable=False)
    severity = Column(String(20), default="MEDIUM")
    description = Column(Text, nullable=False)
    expected_symptoms = Column(Text, nullable=False)
    affected_services = Column(JSON, nullable=True)
    adaptation_flow = Column(Text, nullable=True)
    is_active = Column(Boolean, default=False)

class ApprovalModel(Base):
    """Table 8: approvals (Section 43)"""
    __tablename__ = "approvals"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String(64), ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    action_name = Column(String(64), nullable=False)
    risk_level = Column(String(20), default="HIGH")
    impact_summary = Column(Text, nullable=True)
    safety_notes = Column(Text, nullable=True)
    status = Column(String(32), default="PENDING")  # PENDING, APPROVED, REJECTED
    requested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    decided_at = Column(DateTime, nullable=True)
    decided_by = Column(String(64), default="human_operator")
    rejection_reason = Column(Text, nullable=True)

class RemediationHistoryModel(Base):
    """Table 9: remediation_history (Section 43)"""
    __tablename__ = "remediation_history"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String(64), index=True, nullable=False)
    strategy_name = Column(String(128), nullable=False)
    scenario_id = Column(String(64), nullable=True)
    attempted_action = Column(String(64), nullable=False)
    outcome = Column(String(32), default="SUCCESS")  # SUCCESS, FAILED, ABORTED
    error_details = Column(Text, nullable=True)
    adaptation_reason = Column(Text, nullable=True)
    confidence = Column(Float, default=0.95)
    duration_seconds = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
