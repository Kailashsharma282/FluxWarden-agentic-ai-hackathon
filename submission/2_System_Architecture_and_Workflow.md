# Deliverable 2: System Architecture & Workflow

**Project**: FluxWarden — Autonomous AI Incident Investigation, Recovery & Resilience Agent  
**Author**: Pochiraju Kailash Ram Markandeya Sharma | **Team**: kailashsharma8  
**Hackathon**: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar  

---

## 1. High-Level System Architecture

```
                          ┌────────────────────────────────────────────────────────┐
                          │         PREMIUM FRONTEND COMMAND CENTER (React 18)     │
                          │   Mission Control • Topology • Telemetry • Chaos Lab   │
                          │   Forensics • Mission Chat • Memory • Architecture     │
                          └───────────────────────────┬────────────────────────────┘
                                                      │
                                   HTTP REST & WebSockets (/ws/events)
                                                      │
                                                      ▼
                          ┌────────────────────────────────────────────────────────┐
                          │            FASTAPI AGENT CONTROLLER & GATEWAY          │
                          │        Structured Logging • CORS • Request Router      │
                          └─────────────┬────────────────────────────┬─────────────┘
                                        │                            │
                                        ▼                            ▼
                 ┌──────────────────────────────┐            ┌──────────────────────────────┐
                 │   COGNITIVE DECISION LAYER   │            │     SAFETY & RISK ENGINE     │
                 │   • Mock Provider (Default)  │            │   • 4 Risk Tiers (LOW to     │
                 │   • Google Gemini 1.5/2.0    │            │     CRITICAL)                │
                 │   • OpenAI GPT-4o            │            │   • Human Approval Gating    │
                 │   • Anthropic Claude 3.5     │            │   • Bounded Loop Safeguards  │
                 └──────────────┬───────────────┘            └──────────────┬───────────────┘
                                │                                           │
                                └─────────────────────┬─────────────────────┘
                                                      │
                                                      ▼
                          ┌────────────────────────────────────────────────────────┐
                          │         AGENT ENGINE (12-Phase State Graph)            │
                          │   IDLE ➔ INVESTIGATE ➔ HYPOTHESIZE ➔ PLAN ➔ EXECUTE   │
                          │   ➔ EVALUATE ➔ REPLAN ➔ VERIFY ➔ COMPLETE / FAILED     │
                          └─────────────┬────────────────────────────┬─────────────┘
                                        │                            │
                                        ▼                            ▼
                 ┌──────────────────────────────┐            ┌──────────────────────────────┐
                 │      TOOL REGISTRY (39)      │            │      PERSISTENCE LAYER       │
                 │   • Diagnostics (12)         │            │   • PostgreSQL / SQLite      │
                 │   • Remediation (11)         │            │     (9 Relational Tables)    │
                 │   • Verification (8)         │            │   • Redis Pub/Sub Stream     │
                 │   • Safety & Memory (8)      │            │   • Operational Memory Index │
                 └──────────────┬───────────────┘            └──────────────────────────────┘
                                │
                                ▼
                          ┌────────────────────────────────────────────────────────┐
                          │      SIMULATED CLOUD PRODUCTION ENVIRONMENT            │
                          │   10 Microservices • Ingress Router • Chaos Injector   │
                          │   payment-api • order-db • redis • backup-service ...  │
                          └────────────────────────────────────────────────────────┘
```

---

## 2. The 12-Phase Cognitive State Machine

FluxWarden implements an explicit finite state machine (Section 4 & 5) preventing uncontrolled generative hallucination:

```
[IDLE] ───► [UNDERSTAND_GOAL] ───► [INVESTIGATE] ───► [HYPOTHESIS] ───► [PLAN]
                                                                          │
                        ┌─────────────────────────────────────────────────┴────────┐
                        │                                                          │
                        ▼ (If Tier 3/4 Risk)                                       ▼ (If Tier 1/2 Risk)
              [APPROVAL_PENDING] ◄── Operator Review                               │
                        │                                                          │
                        ▼ (Approved)                                               │
                        └────────────────────────► [EXECUTE] ◄─────────────────────┘
                                                      │
                                                      ▼
                                                 [EVALUATE]
                                                      │
                                       ┌──────────────┴──────────────┐
                                       │ (Action Succeeded)          │ (Action FAILED)
                                       ▼                             ▼
                                   [VERIFY] ◄──────────────────── [REPLAN]
                                       │                        (Adapts Strategy)
                         ┌─────────────┴─────────────┐
                         │ (All 6 Probes Pass)       │ (Probes Fail)
                         ▼                           ▼
                    [COMPLETE]                    [FAILED]
              (Resolution Card & Post-Mortem) (Human SRE Escalation)
```

### State Definitions:
1. **`IDLE`**: Baseline state; monitors telemetry heartbeat.
2. **`UNDERSTAND_GOAL`**: Parses incoming natural language objectives and extracts invariant safety constraints (e.g., zero data loss).
3. **`INVESTIGATE`**: Dispatches read-only diagnostic tools (`get_service_health`, `get_recent_logs`, `get_metrics`).
4. **`HYPOTHESIS`**: Synthesizes evidence to isolate the fault domain and suspect release/configuration commit.
5. **`PLAN`**: Formulates the initial remediation strategy.
6. **`APPROVAL_PENDING`**: Halts execution if action is classified as High Risk; requests human authorization.
7. **`EXECUTE`**: Dispatches approved sandboxed remediation action.
8. **`EVALUATE`**: Examines tool return codes and system health metrics to check for anomalies.
9. **`REPLAN`**: **The Core Differentiating State**. Triggered when remediation fails. Updates failed action memory, inspects topology for alternate paths (e.g., standby replica failover), and pivots strategy.
10. **`VERIFY`**: Engages the independent 6-probe verification suite.
11. **`COMPLETE`**: Compiles forensic post-mortem report, updates Operational Memory, and displays glowing resolution celebration card.
12. **`FAILED`**: Safe boundary termination if retry limits or step counts (`MAX_AGENT_STEPS`) are exceeded.

---

## 3. Tool Registry Architecture (39 Tools)

Tools are sandboxed and strictly schema-validated:
- **Diagnostic Tools (12)**: `get_service_health`, `get_recent_logs`, `get_metrics`, `get_recent_deployments`, `get_service_dependencies`, `get_backup_status`, `query_audit_logs`, etc.
- **Remediation Tools (11)**: `rollback_deployment`, `route_traffic`, `scale_service`, `restart_service`, `clear_cache`, `failover_service`, `drain_connections`, etc.
- **Verification Tools (8)**: `verify_service_recovery`, `run_synthetic_smoke_test`, `check_latency_sla`, `check_error_rate_sla`, `verify_db_acid_integrity`, etc.
- **Safety & Memory Tools (8)**: `request_human_approval`, `record_failed_action`, `query_operational_memory`, `store_incident_resolution`, `create_incident_report`, etc.

---

## 4. Simulated Production Topology (10 Microservices)

FluxWarden interacts with a live simulated Kubernetes/Cloud production topology:
1. **`api-gateway`**: Edge ingress reverse proxy.
2. **`auth-service`**: OAuth2/JWT token verification service.
3. **`payment-api`**: High-throughput transaction processor (Target of Scenario A).
4. **`order-service`**: Order workflow coordinator.
5. **`inventory-service`**: Real-time warehouse catalog inventory.
6. **`notification-service`**: Async email and SMS notification dispatcher.
7. **`order-db`**: Primary PostgreSQL ACID database cluster.
8. **`redis-cache`**: In-memory session and transaction lock store.
9. **`backup-service`**: **Synchronized hot-standby replica** (v40-stable) ready for instant failover traffic absorption.
10. **`deployment-controller`**: CI/CD rollout and container orchestration manager.
