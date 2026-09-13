# Deliverable 4: Demonstration Videos & Audio Voiceover Scripts

**Project**: FluxWarden — Autonomous AI Incident Investigation, Recovery & Resilience Agent  
**Author**: Pochiraju Kailash Ram Markandeya Sharma | **Team**: kailashsharma8  
**Hackathon**: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar  

---

## 1. Master Demonstration Video (3–5 Minute Deliverable)

### 🌟 `fluxwarden_master_demo.mp4`
- **Format**: MP4 (H.264 Video / AAC Audio, 1920x924 @ 20fps)
- **Duration**: **3 minutes 42 seconds** (Strictly within the 3–5 minute requirement)
- **File Size**: `10.77 MB`
- **Location**: [`submission/4_Demo_Videos/fluxwarden_master_demo.mp4`](fluxwarden_master_demo.mp4) (also in [`docs/recordings/fluxwarden_master_demo.mp4`](../../docs/recordings/fluxwarden_master_demo.mp4))

This continuous presentation combines all three core facets of the platform:
1. **0:00 – 1:00**: Platform Overview & Command Center Walkthrough (Canvas Topology, Live Telemetry).
2. **1:00 – 2:30**: Deterministic Incident Recovery (Bad Deployment, Rollback Failure, Cognitive Replanning, Standby Traffic Rerouting, 6-Probe Verification Engine).
3. **2:30 – 3:42**: Chaos Lab Injection, Mission Chat Objective Parsing, and Human-in-the-Loop Safety Approval Modal.

---

## 2. Individual Demonstration Videos

| Demonstration | MP4 File | Duration | File Size | Description |
|---|---|---|---|---|
| **Demo 1: Platform Tour** | `demo_1_overview.mp4` | 1m 41s | 8.9 MB | Command Center tour across all 8 navigation tabs |
| **Demo 2: Adaptive Recovery** | `demo_2_adaptive_recovery.mp4` | 2m 00s | 3.3 MB | 15-step sequence with rollback failure, replanning & probes |
| **Demo 3: Chaos & Approval** | `demo_3_chaos_approval.mp4` | 1m 28s | 10.5 MB | Chaos scenario injection, natural language chat & human gating |

---

## 3. Full Synchronized Voiceover Transcripts

### Demonstration 1: Platform Overview & Command Center Walkthrough
> *"Welcome to FluxWarden, an autonomous agentic AI platform for enterprise incident investigation, adaptive recovery, and system resilience. Presented by Kailash Sharma for the Agentic AI Hackathon at Tech Zephyr 4.0, IIT Bhubaneswar.*
> 
> *In this first demonstration, we tour the Command Center interface. The Mission Control view displays the live autonomous state machine, currently in Idle and ready for operational dispatch. Navigating to Service Topology reveals our live Canvas visualization with ten interconnected microservices, dependency directed graphs, and pulsing packet flows. Switching to Live Telemetry, we monitor real-time request rates, error rates, and p99 latency across all services, streaming at one thousand six hundred requests per second.*
> 
> *The Chaos Lab provides one-click injection for realistic failure scenarios, including bad deployments, database connection exhaustion, memory leaks, and cascading failures. Under Incident Forensics, engineers can review root cause analyses, failure timeline events, hypotheses, and forensic evidence logs. The Mission Chat interface allows operators to converse with the agent in natural language and grant human approvals for high-risk remediation actions. Operational Memory indexes past incidents and learned resolution strategies using semantic retrieval. Finally, the Architecture and Judge Scorecard tabs provide interactive component inspection and confirm complete compliance with all sixty-eight hackathon requirements."*

---

### Demonstration 2: Deterministic Incident Recovery & Adaptive Replanning
> *"This is Demonstration Two: Deterministic Incident Recovery and Adaptive Replanning. We trigger the live demonstration sequence by clicking RUN DEMO.*
> 
> *Step One: A bad deployment is injected into the payment API. The error rate instantly spikes to seventy-four percent, and service health transitions to critical red. Steps Two through Five: FluxWarden autonomously begins investigation. The agent queries service health, inspects recent container logs, and detects an uncaught null pointer exception introduced in release v42.*
> 
> *Step Six demonstrates our critical differentiating capability: The agent initiates a standard rollback to release v41, but the rollback intentionally fails because the container image is corrupted in the registry. A static script would crash or loop indefinitely. But FluxWarden detects the tool failure, updates its failed actions history, and dynamically transitions to the Replan state.*
> 
> *Steps Seven to Nine: The agent inspects operational memory and queries standby backup services, discovering that backup-service v40 is healthy and synchronized. Step Ten: The agent executes adaptive recovery, rerouting ingress traffic from the failed payment API to the standby backup replica. The live topology canvas reflects the immediate traffic shift.*
> 
> *Steps Eleven through Fourteen: The six-probe verification engine engages, executing synthetic transactions, latency SLA checks, error rate monitoring, dependency probes, and database ACID consistency validations. Step Fifteen: All six verification probes pass with flying colors. The glowing incident resolution card appears, detailing the root cause, failed rollback, successful adaptive recovery, and post-mortem report ready for export."*

---

### Demonstration 3: Chaos Lab Injection, Mission Chat & Human Approval Gating
> *"This is Demonstration Three: Chaos Lab Scenario Injection, Mission Chat, and Human-in-the-Loop Safety Controls. Section 17 of our design specification requires strict human authorization for high-risk infrastructure interventions.*
> 
> *We enter the Chaos Lab and inject a high-severity Database Connection Pool Exhaustion incident into order-db. The active connection count spikes to ninety-nine percent, thread pools deadlock, and API gateway requests begin queuing. Switching to Mission Chat, the operator prompts the agent: 'Investigate order database deadlock and execute emergency connection drain and restart.'*
> 
> *FluxWarden parses the objective, evaluates safety boundaries, and identifies that restarting a core database is a High Risk Tier Three action. Instead of proceeding unilaterally, the agent halts and surfaces the Human Approval Modal. The modal displays the blast radius, targeted resources, rollback safety plan, and justification.*
> 
> *The human operator reviews the proposed action and clicks Approve Action. With authorization granted, the agent executes the connection pool drain, safely restarts the database instance, and confirms recovery via telemetry probes. FluxWarden seamlessly balances full agentic autonomy with enterprise-grade safety and human oversight."*
