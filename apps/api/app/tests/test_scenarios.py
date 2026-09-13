from app.simulations.environment import sim_env

def test_scenario_injection_and_reset():
    sim_env.reset_environment()
    assert sim_env.services["payment-api"].status == "healthy"
    assert sim_env.active_scenario is None

    # Inject Bad Deployment
    res = sim_env.inject_scenario("bad_deployment")
    assert res["scenario"] == "bad_deployment"
    assert sim_env.services["payment-api"].status == "unhealthy"
    assert sim_env.services["payment-api"].version == "v42"
    assert sim_env.services["payment-api"].error_rate >= 0.70

    # Inject DB Connection Exhaustion
    res_db = sim_env.inject_scenario("db_connection_exhaustion")
    assert res_db["scenario"] == "db_connection_exhaustion"
    assert sim_env.services["postgres"].configuration["active_connections"] == 498

    # Reset
    sim_env.reset_environment()
    assert sim_env.services["payment-api"].status == "healthy"
    assert sim_env.services["postgres"].status == "healthy"
    assert sim_env.active_scenario is None
