# FluxWarden REST & WebSocket API Reference

**Author**: Pochiraju Kailash Ram Markandeya Sharma  
**Team**: kailashsharma8  
**Hackathon**: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar  

---

## REST Endpoints

### 1. Incidents
- `POST /api/incidents`: Create a new incident and initialize agent mission.
- `GET /api/incidents`: List all active and historical incidents.
- `GET /api/incidents/{id}`: Fetch incident metadata and active agent state.
- `POST /api/incidents/{id}/start`: Start autonomous cognitive resolution loop in background.
- `POST /api/incidents/{id}/stop`: Pause or cancel agent execution.
- `GET /api/incidents/{id}/state`: Retrieve current strongly typed `AgentState`.
- `GET /api/incidents/{id}/events`: Retrieve all structured events emitted during resolution.
- `GET /api/incidents/{id}/trace`: Retrieve numbered chronological step execution trace.
- `POST /api/incidents/{id}/approve`: Approve pending high-risk action.
- `POST /api/incidents/{id}/reject`: Reject pending high-risk action and force replanning.

### 2. System & Telemetry
- `GET /api/system/status`: Overall operational status and hackathon metadata.
- `GET /api/system/services`: List all 10 simulated microservices and their health telemetry.
- `GET /api/system/metrics`: Live snapshot of CPU, RAM, latency, error rate, and active database connections.

### 3. Chaos Simulation
- `GET /api/scenarios`: List all available chaos incident scenarios.
- `POST /api/scenarios/inject`: Inject a scenario (e.g. `bad_deployment`, `db_connection_exhaustion`, `redis_outage`).
- `POST /api/scenarios/reset`: Restore all 10 microservices to 100% healthy baseline.

### 4. Interactive Mission & Demo
- `POST /api/chat`: Natural language mission command interface.
- `POST /api/demo/run`: Launch the deterministic end-to-end demo sequence.

---

## WebSocket Endpoints

- `ws://localhost:8000/ws/events`: Real-time streaming channel broadcasting all `AgentEvent` payloads, state transitions, and live terminal logs.
- `ws://localhost:8000/ws/incidents/{id}`: Dedicated incident streaming channel.
