import pytest
from app.verification.engine import verification_engine
from app.simulations.environment import sim_env

@pytest.mark.asyncio
async def test_verification_fails_when_unhealthy():
    sim_env.reset_environment()
    sim_env.inject_scenario("bad_deployment")
    # In bad deployment, payment-api is unhealthy so verification must fail
    res = await verification_engine.verify_incident("INC-VERIF-1")
    assert res.passed is False
    assert res.resolution_status == "STILL_UNHEALTHY"

@pytest.mark.asyncio
async def test_verification_passes_after_traffic_reroute():
    sim_env.reset_environment()
    sim_env.inject_scenario("bad_deployment")
    # Simulate agent routing to backup-service
    sim_env.traffic_target = "backup-service"
    for sname, s in sim_env.services.items():
        s.active_target = (sname == "backup-service")

    res = await verification_engine.verify_incident("INC-VERIF-2")
    assert res.passed is True
    assert res.resolution_status == "RESOLVED"
    assert "health_check" in res.checks
    assert "database_integrity" in res.checks
