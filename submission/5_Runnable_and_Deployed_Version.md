# Deliverable 5: Runnable & Deployed Version Guide

**Project**: FluxWarden — Autonomous AI Incident Investigation, Recovery & Resilience Agent  
**Author**: Pochiraju Kailash Ram Markandeya Sharma | **Team**: kailashsharma8  
**Hackathon**: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar  

---

## 1. Cloud Deployed Version (Render & Vercel)

FluxWarden is configured for instant cloud execution across two resilient tiers:

- **Frontend Command Center (Vercel Edge)**:
  - Deployed URL: `https://<YOUR_VERCEL_PROJECT>.vercel.app`
  - Automated continuous deployment connected to `main` branch.
- **Backend API & Agent Engine (Render Web Service)**:
  - Deployed API URL: `https://<YOUR_RENDER_SERVICE>.onrender.com`
  - Interactive OpenAPI / Swagger Documentation: `https://<YOUR_RENDER_SERVICE>.onrender.com/docs`
  - Realtime Event Stream: `wss://<YOUR_RENDER_SERVICE>.onrender.com/ws/events`
  - System Health Check: `https://<YOUR_RENDER_SERVICE>.onrender.com/health`

*(For 1-click redeployment instructions, refer to [`docs/deployment-guide.md`](../docs/deployment-guide.md)).*

---

## 2. Local Runnable Version (Zero-Configuration Clean Checkout)

In compliance with Section 64 of the specification, FluxWarden runs on a clean checkout with **zero pre-existing database configuration or external API keys required**.

### Method A: Standalone Single-Command Runner (Fastest)

Prerequisites: Python 3.11+ and Node.js 18+.

```bash
# 1. Clone the repository
git clone https://github.com/Kailashsharma282/FluxWarden-agentic-ai-hackathon.git
cd FluxWarden-agentic-ai-hackathon

# 2. Run the single startup command
python run_dev.py
```

`run_dev.py` automatically:
1. Installs backend dependencies if missing.
2. Initializes SQLite database and seeds 9 tables (10 services, 6 scenarios, historical memory).
3. Launches the FastAPI backend daemon on `http://127.0.0.1:8001`.
4. Installs frontend npm packages and launches Vite on `http://localhost:3000`.
5. Opens your default web browser to the Command Center.

---

### Method B: Full Production Docker Compose (All 11 Services)

Prerequisites: Docker and Docker Compose.

```bash
# Launch all 11 services with health checks
docker compose up --build
```

Access Points:
- **Frontend Dashboard**: `http://localhost:3000`
- **Backend API & Swagger**: `http://localhost:8000/docs`
- **PostgreSQL**: `localhost:5432` (`postgres:fluxwarden_pass`)
- **Redis**: `localhost:6379`

---

## 3. Step-by-Step Judge Demonstration Flow

To reproduce the full capability within 3 minutes:

1. **Open Dashboard**:
   Navigate to `http://localhost:3000` and click **Launch Command Center**.
2. **Review Baseline Health**:
   Observe the **Service Topology** canvas showing 10 green, operational services with active packet traffic lines.
3. **Execute Deterministic Demo**:
   Click the **RUN DEMO** button in the top navigation bar (or press `D`).
   - *Step 01*: Bad Deployment injected (`payment-api` error rate spikes to 74%).
   - *Steps 02–05*: Agent queries logs and CI/CD history, detecting the v42 regression.
   - *Step 06*: **Rollback Fails** (pulses red due to corrupted registry image).
   - *Steps 07–09*: Agent **Replans**, queries operational memory, and discovers `backup-service`.
   - *Step 10*: Traffic rerouted to `backup-service`; topology packet streams dynamically redirect.
   - *Steps 11–14*: 6-probe verification runs sequentially (all pass).
   - *Step 15*: Glowing **Incident Resolved** celebration card appears.
4. **Export Forensic Artifacts**:
   Navigate to **Incident Forensics** (or click the card buttons) to view all 11 collapsible sections. Click **Export JSON**, **Export Markdown**, or **Print / Save PDF Report**.
5. **Test Chaos Lab & Safety Approval**:
   Switch to **Chaos Lab**, inject *Database Connection Exhaustion*, open **Mission Chat**, prompt: *"Perform emergency database restart"*, and observe the **Human Approval Modal** gate the high-risk action until approved by the operator.
