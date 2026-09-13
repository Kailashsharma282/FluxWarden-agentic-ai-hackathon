import pytest
from app.tools.registry import tool_registry
from app.simulations.environment import sim_env

@pytest.mark.asyncio
async def test_tool_registry_diagnostics():
    sim_env.reset_environment()
    res = await tool_registry.execute("get_service_status", {"service_name": "payment-api"})
    assert res.success is True
    assert res.data["status"] == "healthy"

    res_logs = await tool_registry.execute("get_recent_logs", {"service_name": "payment-api", "limit": 5})
    assert res_logs.success is True
    assert "logs" in res_logs.data

    res_db = await tool_registry.execute("get_database_health", {})
    assert res_db.success is True
    assert res_db.data["service"] == "postgres"

@pytest.mark.asyncio
async def test_tool_registry_intentional_rollback_failure():
    sim_env.reset_environment()
    sim_env.inject_scenario("bad_deployment")
    # Rollback must fail intentionally in Bad Deployment scenario
    res = await tool_registry.execute("rollback_deployment", {"service_name": "payment-api"})
    assert res.success is False
    assert "Rollback failed" in res.error

@pytest.mark.asyncio
async def test_tool_registry_traffic_reroute():
    sim_env.reset_environment()
    res = await tool_registry.execute("route_traffic", {"target_service": "backup-service"})
    assert res.success is True
    assert sim_env.traffic_target == "backup-service"

@pytest.mark.asyncio
async def test_unknown_tool_handling():
    res = await tool_registry.execute("non_existent_tool_xyz", {})
    assert res.success is False
    assert "Unknown tool" in res.error
