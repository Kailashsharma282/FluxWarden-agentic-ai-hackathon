import pytest
from app.agents.engine import AgentEngine
from app.agents.state_graph import StateTransitionEngine, AgentStatePhase
from app.simulations.environment import sim_env

def test_state_transitions():
    assert StateTransitionEngine.can_transition("IDLE", "UNDERSTAND_GOAL") is True
    assert StateTransitionEngine.can_transition("UNDERSTAND_GOAL", "INVESTIGATE") is True
    assert StateTransitionEngine.can_transition("EVALUATE", "REPLAN") is True
    assert StateTransitionEngine.can_transition("EVALUATE", "VERIFY") is True
    assert StateTransitionEngine.can_transition("IDLE", "EXECUTE") is False

@pytest.mark.asyncio
async def test_agent_cognitive_adaptation_flow():
    engine = AgentEngine()
    sim_env.reset_environment()
    sim_env.inject_scenario("bad_deployment")

    # 1. Initialize mission
    state = await engine.initialize_mission(
        user_goal="The payment API is failing. Investigate the cause and restore service without causing data loss.",
        incident_id="INC-TEST-01"
    )
    assert state.current_phase == "INVESTIGATE"

    # 2. Step 1: Query service health
    state = await engine.step()
    assert "get_service_health" in state.completed_actions

    # 3. Step 2: Inspect recent logs
    state = await engine.step()
    assert "get_recent_logs" in state.completed_actions

    # 4. Step 3: Inspect deployment history -> Anomaly detected!
    state = await engine.step()
    assert "get_recent_deployments" in state.completed_actions
    assert state.current_phase == "HYPOTHESIS"

    # 5. Step 4: Attempt Rollback -> MUST FAIL INTENTIONALLY (Image unavailable in registry)
    state = await engine.step()
    assert len(state.failed_actions) == 1
    assert state.failed_actions[0]["tool"] == "rollback_deployment"
    assert state.current_phase == "REPLAN"
    assert state.replan_count == 1

    # 6. Step 5: Adapt -> Check Backup Readiness
    state = await engine.step()
    assert "get_backup_status" in state.completed_actions

    # 7. Step 6: Route Traffic to Healthy Standby Backup & Run Verification
    state = await engine.step()
    assert "route_traffic" in state.completed_actions
    assert state.resolution_status == "RESOLVED"
    assert state.current_phase == "COMPLETE"
    assert state.final_report is not None
    assert "standby replica" in state.final_report["recovery_strategy"].lower()

@pytest.mark.asyncio
async def test_agent_human_approval_flow():
    engine = AgentEngine()
    sim_env.reset_environment()
    await engine.initialize_mission("Resolve Redis cache outage", incident_id="INC-REDIS-01")
    sim_env.inject_scenario("redis_outage")

    # Set phase to HYPOTHESIS so it plans failover_service (HIGH RISK)
    engine.state.current_phase = "HYPOTHESIS"
    engine.state.completed_actions = ["get_service_health", "get_recent_logs"]

    # Step: It should plan failover_service, detect HIGH risk, and pause for approval!
    state = await engine.step()
    assert state.current_phase == "WAITING_FOR_APPROVAL"
    assert state.approval_required is True
    assert state.pending_approval_action is not None
    assert state.pending_approval_action["tool"] == "failover_service"

    # Approve action
    state_after = await engine.approve_pending_action()
    assert state_after.approval_required is False
    assert "failover_service" in state_after.completed_actions

@pytest.mark.asyncio
async def test_agent_max_steps_boundary():
    engine = AgentEngine()
    await engine.initialize_mission("Infinite test mission", incident_id="INC-LIMIT-01")
    engine.state.attempt_count = 15  # Reached MAX_AGENT_STEPS

    state = await engine.step()
    assert state.current_phase == "FAILED"
    assert state.resolution_status == "ESCALATED"

@pytest.mark.asyncio
async def test_agent_invalid_tool_resilience():
    """Section 53 Agent test: verify agent handles invalid/unknown tool safely."""
    engine = AgentEngine()
    await engine.initialize_mission("Test unknown tool safety", incident_id="INC-INV-01")

    # Mock provider returning an unknown tool
    class BadToolProvider:
        async def decide_next_step(self, context):
            from app.agents.providers import LLMActionPlan
            return LLMActionPlan(
                phase="EXECUTE",
                thought_summary="Testing invalid tool call",
                current_action="Invoke invalid tool",
                why="Testing resilience",
                expected_result="Safe handling",
                tool_to_execute="non_existent_chaos_tool"
            )

    engine.llm_provider = BadToolProvider()
    state = await engine.step()
    assert len(state.failed_actions) == 1
    assert "non_existent_chaos_tool" in state.failed_actions[0]["tool"]
    assert state.current_phase == "REPLAN"

@pytest.mark.asyncio
async def test_agent_malformed_model_output_retry():
    """Section 53 Agent test: verify agent safely retries structured output schema and halts gracefully."""
    engine = AgentEngine()
    await engine.initialize_mission("Test malformed output", incident_id="INC-MAL-01")

    class MalformedProvider:
        async def decide_next_step(self, context):
            raise ValueError("Malformed model JSON: unexpected token at line 1")

    engine.llm_provider = MalformedProvider()
    state = await engine.step()
    assert state.current_phase == "FAILED"
    assert state.resolution_status == "ESCALATED"

@pytest.mark.asyncio
async def test_agent_failed_recovery():
    """Section 53 Agent test: verify handling when remediation repeatedly fails."""
    engine = AgentEngine()
    await engine.initialize_mission("Test repeated failure", incident_id="INC-FAIL-01")
    engine.state.replan_count = 3  # MAX_REPLAN_ATTEMPTS reached

    state = await engine.step()
    # Agent detects max replan attempts and halts safely
    assert state.attempt_count > 0
