# FluxWarden Architecture & System Design

**Author**: Pochiraju Kailash Ram Markandeya Sharma (Solo Participant)  
**Team**: kailashsharma8  
**Hackathon**: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar  

FluxWarden is an autonomous AI incident response and infrastructure resilience system designed to bridge the gap between static alert triage and intelligent, adaptive remediation.

---

## High-Level Architecture

```
                               ┌─────────────────────────┐
                               │       OPERATOR / UI     │
                               │ (Command Center & Chat) │
                               └────────────┬────────────┘
                                            │ HTTP / WebSocket
                                            ▼
                               ┌─────────────────────────┐
                               │   FastAPI Gateway API   │
                               │  (/api/incidents, /ws)  │
                               └────────────┬────────────┘
                                            │
                                            ▼
                               ┌─────────────────────────┐
                               │   AGENT CONTROLLER      │
                               │  (Cognitive Loop / FSM) │
                               └────────────┬────────────┘
                                            │
         ┌──────────────────────────────────┴──────────────────────────────────┐
         │                                                                     │
         ▼                                                                     ▼
┌──────────────────┐                                                  ┌──────────────────┐
│   STATE GRAPH    │                                                  │  TOOL REGISTRY   │
│ (Explicit Finite │                                                  │  (39 Tools:      │
│  State Machine)  │                                                  │   Diagnostics,   │
└────────┬─────────┘                                                  │   Remediation,   │
         │                                                            │   Verification,  │
         │                                                            │   Safety)        │
         ▼                                                            └────────┬─────────┘
┌──────────────────┐                                                           │
│ DECISION ENGINE  │                                                           │
│ (Mock, OpenAI,   │                                                           │
│  Gemini, Claude) │                                                           │
└────────┬─────────┘                                                           │
         │                                                                     │
         └──────────────────────────────────┬──────────────────────────────────┘
                                            │ Dispatches Actions & Gathers Telemetry
                                            ▼
                               ┌─────────────────────────┐
                               │   SIMULATED PROD ENV    │
                               │ (10 Microservices,      │
                               │  Traffic Router, Mesh)  │
                               └────────────┬────────────┘
                                            │
                     ┌──────────────────────┴──────────────────────┐
                     │                                             │
                     ▼                                             ▼
          ┌─────────────────────┐                       ┌─────────────────────┐
          │ VERIFICATION ENGINE │                       │     RISK ENGINE     │
          │ (6-Probe Independent│                       │ (LOW, MEDIUM, HIGH, │
          │  Verification Suite)│                       │  CRITICAL Guardrails│
          └─────────────────────┘                       └─────────────────────┘
```

---

## Core Components

### 1. Goal Interpreter & Cognitive Loop
Receives high-level human objectives such as:
> *"The payment API is failing. Investigate the cause and restore service without causing data loss."*

Unlike simple chatbots or hardcoded scripts, FluxWarden dynamically plans sub-actions, observes outcomes, and updates its internal state model.

### 2. Explicit State Machine (State Graph)
The agent operates through strictly bounded states:
- `IDLE`
- `UNDERSTAND_GOAL`
- `INVESTIGATE`
- `HYPOTHESIS`
- `PLAN`
- `EXECUTE`
- `EVALUATE`
- `REPLAN`
- `WAITING_FOR_APPROVAL`
- `VERIFY`
- `COMPLETE`
- `FAILED`

### 3. Verification Engine
An action returning `{"success": true}` is **never** accepted as proof of incident resolution. The Verification Engine executes 6 independent probes:
1. Health & Liveness Probe
2. Synthetic Smoke Test
3. Error Rate SLA Check (<5%)
4. Latency SLA Check (<200ms)
5. Dependency Health Check
6. Database ACID Transaction & Connection Integrity Check

Only when all 6 probes succeed does `resolution_status` transition to `RESOLVED`.
