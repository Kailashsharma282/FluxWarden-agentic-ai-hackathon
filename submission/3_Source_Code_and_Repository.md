# Deliverable 3: Source Code & Repository

**Project**: FluxWarden — Autonomous AI Incident Investigation, Recovery & Resilience Agent  
**Author**: Pochiraju Kailash Ram Markandeya Sharma | **Team**: kailashsharma8  
**Hackathon**: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar  

---

## 1. Official Repository Details

- **GitHub Repository**: [https://github.com/Kailashsharma282/FluxWarden-agentic-ai-hackathon.git](https://github.com/Kailashsharma282/FluxWarden-agentic-ai-hackathon.git)
- **Primary Branch**: `main`
- **Latest Verified Commit**: `2225287`
- **License**: MIT Open Source

---

## 2. Confidentiality & Security Audit (Zero Credentials)

In compliance with the hackathon rule:
> *"Teams must not include API keys, passwords, tokens, or other confidential credentials in their repository."*

An automated security audit of the repository verifies:
- **0** hardcoded API keys (OpenAI, Gemini, Anthropic).
- **0** database passwords or JWT secrets.
- **0** private keys or cloud credentials.
- All configuration parameters use standard environment variable patterns defined in [`.env.example`](../.env.example).
- The application executes fully offline with the built-in `MockLLMProvider` requiring **zero credentials**.

---

## 3. Codebase File Structure

```
FluxWarden/
├── apps/
│   ├── api/                           # Backend FastAPI & Cognitive Engine
│   │   ├── app/
│   │   │   ├── agents/                # Cognitive Loop, FSM Graph & Multi-LLM Providers
│   │   │   ├── api/                   # REST Routes (incidents, system, scenarios, chat, demo, ws)
│   │   │   ├── database/              # SQLAlchemy Async Models (9 tables), Migrations & Seed
│   │   │   ├── memory/                # Operational Memory (Incident pattern vector store)
│   │   │   ├── models/                # Pydantic state models & event definitions
│   │   │   ├── safety/                # Risk Engine (4 Tiers) & Action Permissibility
│   │   │   ├── schemas/               # Strongly-typed request/response validation schemas
│   │   │   ├── services/              # Incident & Telemetry domain persistence services
│   │   │   ├── simulations/           # 10-Node Microservice Cloud Environment Simulation
│   │   │   ├── tests/                 # Full Pytest Automated Test Suite (19 tests)
│   │   │   ├── tools/                 # Sandboxed Tool Registry (39 discrete tools)
│   │   │   └── verification/          # 6-Probe Independent Verification Engine
│   │   ├── Dockerfile                 # Multi-stage Python 3.11 container image
│   │   └── requirements.txt           # Pinned production backend dependencies
│   │
│   └── web/                           # Frontend SRE Command Center (React 18 & Vite)
│       ├── src/
│       │   ├── animations/            # Framer Motion state transition presets (Section 48)
│       │   ├── app/                   # Root App component & theme provider
│       │   ├── components/            # Navbar, CommandPalette, ApprovalModal, BackgroundCanvas
│       │   ├── features/              # MissionControl, Topology, Telemetry, ChaosLab,
│       │   │                          # Forensics, MissionChat, Memory, Architecture, Settings
│       │   ├── hooks/                 # useAgentEvents (WebSocket), useKeyboardShortcuts
│       │   ├── lib/                   # utils.ts (formatters) & constants.ts (app limits)
│       │   ├── services/              # api.ts (REST client & auto-reconnecting WebSocket)
│       │   ├── types/                 # TypeScript interfaces for all state & events
│       │   └── visualizations/        # HTML5 Canvas Topology & Metric Chart visualizers
│       ├── package.json               # Frontend dependencies & npm test scripts
│       └── vite.config.ts             # Dev server & API proxy configuration
│
├── docs/                              # Exhaustive Technical Documentation
│   ├── architecture.md                # System design & component interaction
│   ├── agent-design.md                # 12-phase finite state machine & cognitive loops
│   ├── tool-system.md                 # 39 sandboxed tools catalog & schemas
│   ├── failure-scenarios.md           # 6 chaos engineering incident scenarios
│   ├── safety-model.md                # 4-tier risk classification & human-in-the-loop
│   ├── demo-script.md                 # Timed chronological presenter narration script
│   ├── deployment-guide.md            # Render (backend) & Vercel (frontend) deploy instructions
│   ├── qa-report.md                   # Complete 24-deliverable compliance validation report
│   └── recordings/                    # Pre-recorded MP4 demos & WAV audio tracks
│
├── docker-compose.yml                 # 11-service local orchestration with healthchecks
├── Makefile                           # Developer workflow (up, down, test, seed, demo)
├── render.yaml                        # 1-Click Render Cloud Backend Blueprint
├── vercel.json                        # 1-Click Vercel Cloud Frontend Configuration
└── run_dev.py                         # Single-command local startup script
```

---

## 4. Automated Testing & Verification Results

### Backend Automated Test Suite (`pytest -v`)
```
============================= 19 passed in 26.82s =============================
apps/api/app/tests/test_agent_graph.py::test_state_transitions PASSED                    [  5%]
apps/api/app/tests/test_agent_graph.py::test_agent_cognitive_adaptation_flow PASSED      [ 10%]
apps/api/app/tests/test_agent_graph.py::test_agent_human_approval_flow PASSED           [ 15%]
apps/api/app/tests/test_agent_graph.py::test_agent_max_steps_boundary PASSED            [ 21%]
apps/api/app/tests/test_agent_graph.py::test_agent_invalid_tool_resilience PASSED        [ 26%]
apps/api/app/tests/test_agent_graph.py::test_agent_malformed_model_output_retry PASSED   [ 31%]
apps/api/app/tests/test_agent_graph.py::test_agent_failed_recovery PASSED                [ 36%]
apps/api/app/tests/test_api.py::test_api_system_endpoints PASSED                         [ 42%]
apps/api/app/tests/test_api.py::test_api_scenario_injection_and_reset PASSED             [ 47%]
apps/api/app/tests/test_api.py::test_api_incident_lifecycle PASSED                       [ 52%]
apps/api/app/tests/test_api.py::test_api_chat_and_demo PASSED                            [ 57%]
apps/api/app/tests/test_risk_engine.py::test_risk_classification PASSED                  [ 63%]
apps/api/app/tests/test_scenarios.py::test_scenario_injection_and_reset PASSED           [ 68%]
apps/api/app/tests/test_tools.py::test_tool_registry_diagnostics PASSED                  [ 73%]
apps/api/app/tests/test_tools.py::test_tool_registry_intentional_rollback_failure PASSED [ 78%]
apps/api/app/tests/test_tools.py::test_tool_registry_traffic_reroute PASSED             [ 84%]
apps/api/app/tests/test_tools.py::test_unknown_tool_handling PASSED                      [ 89%]
apps/api/app/tests/test_verification.py::test_verification_fails_when_unhealthy PASSED  [ 94%]
apps/api/app/tests/test_verification.py::test_verification_passes_after_traffic_reroute PASSED [100%]
```

### Frontend Verification (`npm test` & `npm run build`)
- **Component Smoke Tests**: **27 of 27** React components verified.
- **Production Build**: **1,894 modules transformed**, built in 12.14s with 0 errors.
