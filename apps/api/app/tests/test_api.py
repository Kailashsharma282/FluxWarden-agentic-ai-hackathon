import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.simulations.environment import sim_env

@pytest.mark.asyncio
async def test_api_system_endpoints():
    sim_env.reset_environment()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Root check
        res = await client.get("/")
        assert res.status_code == 200
        data = res.json()
        assert data["name"] == "FluxWarden"
        assert "Pochiraju Kailash Ram Markandeya Sharma" in data["participant"]
        assert "kailashsharma8" in data["team"]

        # Health check
        res_h = await client.get("/health")
        assert res_h.status_code == 200

        # System services
        res_svc = await client.get("/api/system/services")
        assert res_svc.status_code == 200
        assert len(res_svc.json()["services"]) == 10

        # System status
        res_st = await client.get("/api/system/status")
        assert res_st.status_code == 200
        assert res_st.json()["overall_status"] == "OPERATIONAL"

@pytest.mark.asyncio
async def test_api_scenario_injection_and_reset():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # List scenarios
        res_list = await client.get("/api/scenarios")
        assert res_list.status_code == 200
        assert len(res_list.json()["scenarios"]) >= 5

        # Inject bad_deployment
        res_inj = await client.post("/api/scenarios/inject", json={"scenario_id": "bad_deployment"})
        assert res_inj.status_code == 200
        assert res_inj.json()["scenario"] == "bad_deployment"

        # Reset
        res_rst = await client.post("/api/scenarios/reset")
        assert res_rst.status_code == 200
        assert res_rst.json()["status"] == "reset_complete"

@pytest.mark.asyncio
async def test_api_incident_lifecycle():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create incident
        res_cr = await client.post("/api/incidents", json={
            "goal": "Restore payment API without causing data loss",
            "incident_id": "INC-TEST-API"
        })
        assert res_cr.status_code == 200
        assert res_cr.json()["incident"]["id"] == "INC-TEST-API"

        # Get state
        res_st = await client.get("/api/incidents/INC-TEST-API/state")
        assert res_st.status_code == 200

        # Get events
        res_ev = await client.get("/api/incidents/INC-TEST-API/events")
        assert res_ev.status_code == 200

        # Get trace
        res_tr = await client.get("/api/incidents/INC-TEST-API/trace")
        assert res_tr.status_code == 200

        # Start incident execution
        res_start = await client.post("/api/incidents/INC-TEST-API/start")
        assert res_start.status_code == 200
        assert res_start.json()["status"] == "started"

        # Stop incident execution
        res_stop = await client.post("/api/incidents/INC-TEST-API/stop")
        assert res_stop.status_code == 200
        assert res_stop.json()["status"] == "stopped"

        # Approve and Reject endpoints
        res_app = await client.post("/api/incidents/INC-TEST-API/approve")
        assert res_app.status_code == 200

        res_rej = await client.post("/api/incidents/INC-TEST-API/reject", json={"reason": "Operator tested reject"})
        assert res_rej.status_code == 200

@pytest.mark.asyncio
async def test_api_chat_and_demo():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Chat endpoint
        res_chat = await client.post("/api/chat", json={"message": "The payment API is failing. Investigate and restore."})
        assert res_chat.status_code == 200
        assert res_chat.json()["sender"] == "FLUXWARDEN"
        assert res_chat.json()["mission_started"] is True

        # Demo endpoint
        res_demo = await client.post("/api/demo/run")
        assert res_demo.status_code == 200
        assert res_demo.json()["status"] == "demo_initiated"

