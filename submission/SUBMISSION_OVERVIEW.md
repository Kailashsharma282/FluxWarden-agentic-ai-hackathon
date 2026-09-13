# FluxWarden: Official Hackathon Submission Package

**Hackathon**: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar  
**Project**: FluxWarden — Autonomous AI Incident Investigation, Recovery & Resilience Agent  
**Participant**: Pochiraju Kailash Ram Markandeya Sharma (Solo Participant)  
**Team Name**: kailashsharma8  
**Repository**: [https://github.com/Kailashsharma282/FluxWarden-agentic-ai-hackathon.git](https://github.com/Kailashsharma282/FluxWarden-agentic-ai-hackathon.git)  
**Latest Verified Commit**: `2225287`  

---

## Submission Checklist & Directory Structure

This submission package is organized strictly according to the five mandatory hackathon deliverables:

```
FluxWarden_Hackathon_Submission/
├── SUBMISSION_OVERVIEW.md                 # This master index document
├── 1_Problem_and_Solution_Brief.md        # Deliverable 1: Problem statement, market impact & agentic solution
├── 2_System_Architecture_and_Workflow.md  # Deliverable 2: Cognitive state machine, tool registry & safety
├── 3_Source_Code_and_Repository.md        # Deliverable 3: Clean source tree, GitHub repository & zero-secret audit
├── 4_Demo_Videos/                         # Deliverable 4: 3–5 Minute MP4 Video Demonstrations with Audio
│   ├── fluxwarden_master_demo.mp4         # ⭐ 3m 42s Master Presentation Video (H.264 + AAC)
│   ├── demo_1_overview.mp4                # 1m 41s Platform Overview & Command Center Tour
│   ├── demo_2_adaptive_recovery.mp4       # 2m 00s Deterministic Recovery & Rollback Replanning
│   ├── demo_3_chaos_approval.mp4          # 1m 28s Chaos Lab, Mission Chat & Human Approval
│   └── DEMO_NARRATION_SCRIPTS.md          # Full synchronized voiceover transcripts with timestamps
├── 5_Runnable_and_Deployed_Version.md     # Deliverable 5: Live Cloud Deployment & Local Execution Guide
├── apps/                                  # Full application source code
│   ├── api/                               # FastAPI Async Agent Engine & PostgreSQL models
│   └── web/                               # React 18, TypeScript, Tailwind CSS, Framer Motion
├── docs/                                  # Complete engineering & QA documentation (24 deliverables)
├── docker-compose.yml                     # 11-service local orchestration with healthchecks
├── render.yaml                            # 1-Click Render Cloud Backend Blueprint
├── vercel.json                            # 1-Click Vercel Cloud Frontend Configuration
└── run_dev.py                             # Single-command local launch script
```

---

## Executive Summary of the Five Deliverables

| Deliverable | Key Highlights | Location in Submission |
|---|---|---|
| **1. Problem & Solution Brief** | Solves alert fatigue and brittle runbooks ($300k/hr downtime) via Goal-driven Autonomous SRE AI with cognitive replanning and multi-probe verification. | [`1_Problem_and_Solution_Brief.md`](1_Problem_and_Solution_Brief.md) |
| **2. System Architecture** | 12-phase finite state machine, 39 sandboxed tools, 10 simulated microservices, 4-tier risk engine, operational memory, and real-time WebSocket telemetry. | [`2_System_Architecture_and_Workflow.md`](2_System_Architecture_and_Workflow.md) |
| **3. Source Code & GitHub** | 100% complete source code on GitHub. Zero credentials/keys included. 19/19 pytest tests passed, 27/27 frontend tests passed, clean Vite build. | [`3_Source_Code_and_Repository.md`](3_Source_Code_and_Repository.md) |
| **4. 3–5 Minute Demo Video** | Standard MP4 (H.264 + AAC), 3 minutes 42 seconds duration. Shows real bad deployment, intentional rollback failure, autonomous replan, traffic reroute, and 6 verification probes. | [`4_Demo_Videos/fluxwarden_master_demo.mp4`](4_Demo_Videos/fluxwarden_master_demo.mp4) |
| **5. Runnable / Deployed** | Live cloud deployment ready on Render (Backend) and Vercel (Frontend). Standalone single-command local run (`python run_dev.py`) with zero external dependencies. | [`5_Runnable_and_Deployed_Version.md`](5_Runnable_and_Deployed_Version.md) |

---

## Confidential Credentials Certification
As required by the hackathon submission guidelines:
- **Zero API keys, tokens, or passwords are baked into the codebase or repository.**
- All sensitive configurations use environment variables via `.env.example`.
- FluxWarden defaults to an autonomous `MockLLMProvider` that reproduces genuine cognitive reasoning offline with zero cost or key dependencies. Real LLM providers (Google Gemini, OpenAI, Claude) can be activated dynamically via the UI Settings panel or environment variables.
