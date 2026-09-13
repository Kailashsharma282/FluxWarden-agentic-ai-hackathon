# FluxWarden — Autonomous AI Incident Investigation, Recovery & Resilience Agent

[![Agentic AI Hackathon](https://img.shields.io/badge/Hackathon-Tech%20Zephyr%204.0%20%7C%20IIT%20Bhubaneswar-blue?style=for-the-badge)](https://iitbbs.ac.in)
[![Team](https://img.shields.io/badge/Team-kailashsharma8-8b5cf6?style=for-the-badge)](#team--credits)
[![Solo Participant](https://img.shields.io/badge/Participant-Pochiraju%20Kailash%20Ram%20Markandeya%20Sharma-00f0ff?style=for-the-badge)](#team--credits)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

> **"AI that doesn't just detect failure. It adapts and restores."**  
> *Alternative Tagline: Observe. Decide. Act. Adapt. Recover.*

---

## 1. Project Overview

**FluxWarden** is an autonomous AI incident response and infrastructure resilience engineer operating inside a realistic simulated production environment. 

When modern cloud infrastructure experiences severe degradation—such as a corrupted release rollout, thread exhaustion, or cache failures—traditional automated runbooks fail because real-world systems are unpredictable. When a standard rollback fails due to a missing registry manifest, conventional CI/CD pipelines crash and demand emergency human triage.

FluxWarden solves this by implementing an authentic **autonomous cognitive loop**:
```
GOAL ➔ OBSERVE ➔ DECIDE ➔ ACT ➔ ACTION FAILS ➔ ADAPT ➔ ACT AGAIN ➔ VERIFY ➔ RECOVER
```

The system dynamically chooses tools, maintains a strongly typed internal state model, detects when an action fails, re-plans alternative strategies, executes failovers, independently verifies system health via multi-probe checks, and compiles forensic post-mortems.

---

## 2. Why FluxWarden Is Genuinely Agentic

FluxWarden is **NOT**:
- ❌ A simple chatbot answering questions
- ❌ A static RAG pipeline retrieving documentation
- ❌ A hardcoded sequential workflow (`check_logs() -> check_metrics() -> rollback()`) disguised as an agent

FluxWarden **IS**:
- ✅ **Goal-Driven**: Receives high-level human objectives (*"Restore payment API without causing data loss"*) and independently deduces intermediate sub-goals.
- ✅ **Dynamic Tool Selection**: Queries a real registry of 39 diagnostic, remediation, verification, and safety tools based on evolving telemetry.
- ✅ **Multi-Step Adaptive Execution**: Performs dependent operations and responds dynamically to intermediate outcomes.
- ✅ **True Adaptation on Failure**: When its primary remediation (rollback) intentionally fails because the target image is corrupted, the agent **does not crash**; it re-plans, searches for healthy backups, and reroutes traffic.
- ✅ **Independent Multi-Probe Verification**: Never assumes an action succeeded merely because an API returned HTTP 200. It independently verifies health, synthetic transactions, error rates, latency, and database ACID integrity.
- ✅ **Enterprise Safety & Human-in-the-Loop**: Strict risk hierarchy (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), pause-for-approval gating on high-risk operations, and bounded loop safeguards.

---

## 3. The Central Demonstration: Rollback Fails ➔ Agent Adapts

```
User Goal: "Payment API is failing. Investigate and restore service."
   ↓
Investigate Payment API Telemetry (HTTP 500 error rate 74%, latency 921ms)
   ↓
Inspect Recent Stderr Logs (NullPointerReference in PaymentGateway.processTransaction)
   ↓
Correlate with CI/CD Deployments (Release dep-42 deployed 3m ago)
   ↓
Hypothesis: Bad deployment v42 introduced schema panic
   ↓
Attempt Rollback to v41
   ↓
💥 ROLLBACK FAILS (Container image v41 missing/corrupted in registry)
   ↓
Agent Detects Failure without crashing
   ↓
Agent Enters REPLAN Phase (Queries Operational Memory & Service Topology)
   ↓
Discovers Healthy Backup Instance (backup-service running v40-stable)
   ↓
Executes Alternative Strategy: Routes 100% Ingress Traffic to Backup Replica
   ↓
Runs Independent 6-Probe Verification Engine (Health, Smoke, SLA, DB Integrity)
   ↓
✅ Service Restored (0.001 error rate, 38ms latency)
   ↓
Compiles Forensic Post-Mortem Report & Saves to Operational Memory
```

---

## 4. Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                          FLUXWARDEN COMMAND CENTER                     │
│               (Futuristic Dark Glassmorphism Web Console)              │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / WebSocket (/ws/events)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                             FASTAPI BACKEND                            │
│ ┌──────────────────────┐  ┌──────────────────────┐  ┌────────────────┐ │
│ │   AGENT CONTROLLER   │  │    TOOL REGISTRY     │  │  RISK ENGINE   │ │
│ │  (Cognitive Engine)  │  │ (39 Real Sandboxed)  │  │ (Approval Gate)│ │
│ └──────────┬───────────┘  └──────────┬───────────┘  └───────┬────────┘ │
│            │                         │                      │          │
│            ▼                         ▼                      ▼          │
│ ┌──────────────────────┐  ┌──────────────────────┐  ┌────────────────┐ │
│ │   AGENT STATE FSM    │  │ VERIFICATION ENGINE  │  │  OPERATIONAL   │ │
│ │ (Explicit LangGraph) │  │  (6 Independent)     │  │     MEMORY     │ │
│ └──────────────────────┘  └──────────────────────┘  └────────────────┘ │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Dispatches Sandboxed Actions
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   SIMULATED PRODUCTION ENVIRONMENT                     │
│  [payment-api]       [auth-service]      [order-service]    [postgres] │
│  [redis]             [backup-service]    [monitoring]       [logging]  │
│  [deployment-ctrl]   [traffic-router]                                  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Agent State Machine

```
   IDLE
    ↓
 UNDERSTAND_GOAL
    ↓
 INVESTIGATE ◄────────┐
    ↓                 │
 HYPOTHESIS           │
    ↓                 │
   PLAN               │
    ↓                 │
 [WAITING_FOR_APPROVAL]
    ↓
  EXECUTE
    ↓
  EVALUATE
  ├─── ACTION FAILED ───► REPLAN ───► PLAN
  └─── ACTION SUCCEEDED
            ↓
          VERIFY ─── PROBES FAILED ───► REPLAN
            ↓ (ALL 6 PROBES PASS)
         COMPLETE
```

---

## 6. Real Tool Registry (39 Tools)

| Category | Tools Included | Risk Level |
| :--- | :--- | :--- |
| **Diagnostic (17)** | `get_service_status`, `get_service_health`, `get_recent_logs`, `search_logs`, `get_metrics`, `get_error_rate`, `get_latency`, `get_cpu_usage`, `get_memory_usage`, `get_database_health`, `get_redis_health`, `get_dependency_status`, `get_recent_deployments`, `get_current_configuration`, `inspect_network`, `get_backup_status`, `get_traffic_distribution` | `LOW` |
| **Remediation (9)** | `restart_service`, `rollback_deployment`, `restore_configuration`, `route_traffic`, `scale_service`, `clear_cache`, `failover_service`, `restore_backup`, `disable_dependency` | `LOW` to `HIGH` |
| **Verification (9)**| `run_health_check`, `run_smoke_test`, `run_payment_test`, `check_error_rate`, `check_latency`, `check_dependency_health`, `verify_database_integrity`, `verify_traffic_distribution`, `verify_service_recovery` | `LOW` |
| **Safety (4)** | `request_human_approval`, `create_incident_report`, `escalate_incident`, `close_incident` | `LOW` to `HIGH` |

---

## 7. Failure Scenarios (Chaos Lab Engine)

FluxWarden includes 6 distinct chaos scenarios (Section 15 & 16):
| Scenario | Severity | Symptoms | Expected Agent Strategy |
|---|---|---|---|
| **Bad Deployment** | `CRITICAL` | 74% 5xx error rate, 921ms latency spike, NullPointerReference | Rollback attempted ➔ Fails intentionally ➔ Replans ➔ Reroutes traffic to standby backup replica |
| **DB Connection Exhaustion** | `HIGH` | Postgres pool saturated (498/500 active), thread timeouts | Dynamically scale connection pool and reset client threads |
| **Redis Outage** | `HIGH` | Redis offline, cache miss latency surges | Automatic failover to standby replica and warm active keyspace |
| **Memory Leak** | `MEDIUM` | Memory climbing to 96%, JVM GC pauses of 420ms | Restart service container and tune memory headroom |
| **Dependency Latency** | `MEDIUM` | Upstream order-service delay (2500ms) | Isolate dependency via circuit breaker; activate fallback |
| **Network Latency** | `MEDIUM` | Packet jitter & gateway delay (850ms) | Reconfigure ingress gateway routing and proxy paths |

---

## 8. Safety & Guardrails

- **Zero Arbitrary Host Commands**: All actions operate strictly within the simulation environment.
- **Risk Gating**: High-risk actions (`failover_service`, `restore_backup`) pause the agent and trigger an interactive **Human Approval Modal**.
- **Critical Blocking**: Destructive actions (`delete_data`, `drop_database`) are strictly blocked.
- **Loop Bounding**: Enforces `MAX_AGENT_STEPS = 15`, `MAX_REPLAN_ATTEMPTS = 3`, and `MAX_TOOL_RETRIES = 2`.

---

## 9. Multi-Provider LLM Abstraction

FluxWarden includes a resilient multi-provider abstraction:
- **`mock` (Default)**: Executes the full authentic state graph, failure injection, replanning, and verification **with ZERO external API keys required**.
- **`openai`**: GPT-4o integration with structured JSON outputs.
- **`gemini`**: Gemini 1.5 Flash integration.
- **`anthropic`**: Claude 3.5 Sonnet integration.

---

## 10. Hackathon 3-5 Minute Demo Script
See [`docs/demo-script.md`](docs/demo-script.md) for the timed chronological walkthrough:
- `0:00 - 0:20`: Show healthy baseline topology
- `0:20 - 0:35`: Inject Bad Deployment via Chaos Lab
- `0:35 - 1:10`: Dispatch natural language objective
- `1:10 - 1:40`: Autonomous investigation & hypothesis
- `1:40 - 2:00`: Attempt Rollback
- `2:00 - 2:15`: **Rollback fails intentionally** (Red pulse)
- `2:15 - 2:45`: Agent adapts & replans
- `2:45 - 3:15`: Reroutes traffic to standby backup replica
- `3:15 - 3:40`: Independent 6-probe verification
- `3:40 - 4:00`: Forensic post-mortem report

---

## 11. Known Limitations
- Host-level system operations are simulated inside an isolated sandbox by design for production security.
- Advanced clustering beyond 10 microservices is bounded by the hackathon demonstration scope.
- Cloud provider IAM permission modifications require external operator credentials.

---

## 12. Quickstart & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- (Optional) Docker & Docker Compose

### 1. Clone & Setup
```bash
git clone https://github.com/kailashsharma8/FluxWarden-Agentic-AI-Hackathon.git
cd FluxWarden-Agentic-AI-Hackathon
```

### 2. Backend Setup & Test Suite
```bash
# Install Python dependencies
pip install -r apps/api/requirements.txt

# Run all 19 automated unit, agent, verification, and API tests
pytest -v
```

### 3. Start Backend API
```bash
cd apps/api
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be live at `http://localhost:8000/docs`.

### 4. Start Frontend Command Center
```bash
cd apps/web
npm install
npm test
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 13. One-Command Docker Startup

```bash
docker compose up --build
```
- Frontend UI: `http://localhost:3000`
- FastAPI REST & WebSockets: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

### Makefile Shortcuts
```bash
make up      # Build and run all containers
make down    # Stop all containers
make test    # Run backend & frontend test suites
make seed    # Seed PostgreSQL with services, scenarios, and historical memory
make demo    # Trigger deterministic demo sequence via CLI
make reset   # Reset all services to healthy baseline
```

---

## 14. Keyboard Shortcuts

- `Cmd / Ctrl + K`: Command Palette
- `C`: Open Natural Language Mission Chat
- `R`: Refresh Telemetry & Status
- `D`: Trigger Deterministic Demo Mode

---

## 15. Team & Credits

| Attribute | Details |
| :--- | :--- |
| **Hackathon** | **Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar** |
| **Team Name** | `kailashsharma8` |
| **Participant** | **Pochiraju Kailash Ram Markandeya Sharma** (Solo Participant) |
| **Repository** | `FluxWarden-Agentic-AI-Hackathon` |

