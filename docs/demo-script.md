# FluxWarden Hackathon Demo Script (3 to 5 Minutes)

**Presenter**: Pochiraju Kailash Ram Markandeya Sharma (Solo Participant)  
**Team**: kailashsharma8  
**Hackathon**: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar  
**Project**: FluxWarden — Autonomous AI Incident Investigation, Recovery & Resilience Agent  

---

## Pre-Recorded Demonstration Videos & Audio Voiceovers

The complete video demonstrations are available in standard universal **MP4 format (H.264 + AAC Audio)** and raw WebP streams in [`docs/recordings/`](file:///c:/Users/kaila/OneDrive/Desktop/Projects/FluxWarden-Agentic-AI-Hackathon/docs/recordings):

### 🌟 Unified Master Presentation Video (All 3 Demos Merged)
- **Master Video (MP4)**: [`fluxwarden_master_demo.mp4`](file:///c:/Users/kaila/OneDrive/Desktop/Projects/FluxWarden-Agentic-AI-Hackathon/docs/recordings/fluxwarden_master_demo.mp4) (10.77 MB, 3:42 mins)
- *Combines the full walkthrough, 15-step adaptive incident recovery, and Chaos Lab with human approvals into one continuous presentation video with narration.*

### Individual Demonstration Videos
| Demo | MP4 Video (Universal) | WebP Video | Audio Voiceover | Description |
|---|---|---|---|---|
| **Demo 1** | [`demo_1_overview.mp4`](file:///c:/Users/kaila/OneDrive/Desktop/Projects/FluxWarden-Agentic-AI-Hackathon/docs/recordings/demo_1_overview.mp4) (8.9 MB) | [`demo_1_overview.webp`](file:///c:/Users/kaila/OneDrive/Desktop/Projects/FluxWarden-Agentic-AI-Hackathon/docs/recordings/demo_1_overview.webp) (27.5 MB) | [`demo_1_overview_audio.wav`](file:///c:/Users/kaila/OneDrive/Desktop/Projects/FluxWarden-Agentic-AI-Hackathon/docs/recordings/demo_1_overview_audio.wav) (4.47 MB) | Platform Overview & Command Center Walkthrough |
| **Demo 2** | [`demo_2_adaptive_recovery.mp4`](file:///c:/Users/kaila/OneDrive/Desktop/Projects/FluxWarden-Agentic-AI-Hackathon/docs/recordings/demo_2_adaptive_recovery.mp4) (3.3 MB) | [`demo_2_adaptive_recovery.webp`](file:///c:/Users/kaila/OneDrive/Desktop/Projects/FluxWarden-Agentic-AI-Hackathon/docs/recordings/demo_2_adaptive_recovery.webp) | [`demo_2_adaptive_recovery_audio.wav`](file:///c:/Users/kaila/OneDrive/Desktop/Projects/FluxWarden-Agentic-AI-Hackathon/docs/recordings/demo_2_adaptive_recovery_audio.wav) (5.30 MB) | Deterministic Incident Recovery & Adaptive Replanning (15-step sequence) |
| **Demo 3** | [`demo_3_chaos_approval.mp4`](file:///c:/Users/kaila/OneDrive/Desktop/Projects/FluxWarden-Agentic-AI-Hackathon/docs/recordings/demo_3_chaos_approval.mp4) (10.5 MB) | [`demo_3_chaos_approval.webp`](file:///c:/Users/kaila/OneDrive/Desktop/Projects/FluxWarden-Agentic-AI-Hackathon/docs/recordings/demo_3_chaos_approval.webp) | [`demo_3_chaos_approval_audio.wav`](file:///c:/Users/kaila/OneDrive/Desktop/Projects/FluxWarden-Agentic-AI-Hackathon/docs/recordings/demo_3_chaos_approval_audio.wav) (3.89 MB) | Chaos Lab Scenario Injection, Mission Chat & Human Approval Flow |

---

## Chronological Demo Script

### 0:00 – 0:20 | Show Healthy Infrastructure Baseline
- **Visual**: Command Center Overview dashboard (`http://localhost:3000`).
- **Narration**:
  > "Welcome judges. I am Kailash Sharma representing team kailashsharma8 at Tech Zephyr 4.0, IIT Bhubaneswar. This is FluxWarden, an autonomous agentic AI designed for incident investigation, recovery, and resilience. As you can see on the live infrastructure topology and metrics graph, all 10 simulated microservices are currently green and operational, handling 1,650 requests per second with an error rate under 0.8% and latency at 45ms."

---

### 0:20 – 0:35 | Inject Bad Deployment via Chaos Lab
- **Visual**: Navigate to **Chaos Lab** or press `D` / click **RUN DEMO**.
- **Action**: Click `Inject Incident` on the **BAD DEPLOYMENT** scenario card.
- **Narration**:
  > "Let's introduce chaos. I am triggering Scenario A: Bad Deployment. The deployment controller rolls out version v42 to `payment-api`. Immediately, the error rate breaches 74%, latency spikes to 921ms, and the service status turns red."

---

### 0:35 – 1:10 | Dispatch High-Level Mission Objective
- **Visual**: Open Mission Chat / Natural Language prompt bar.
- **Action**: Submit prompt:
  > *"The payment API is failing. Investigate the cause and restore service without causing data loss."*
- **Narration**:
  > "We do not tell the agent what scripts to run. We give it an open-ended goal with safety constraints: preserve data integrity and restore service. FluxWarden accepts the goal, parses operational constraints, and initializes its explicit state machine."

---

### 1:10 – 1:40 | Autonomous Investigation & Hypothesis Formation
- **Visual**: Watch the **Agent Status Panel**, **Execution Timeline**, and **Live Terminal**.
- **Observations**:
  - Agent calls `get_service_health(payment-api)`
  - Agent queries `get_recent_logs(payment-api)` -> detects `NullPointerReference in PaymentGateway.processTransaction()`
  - Agent checks `get_recent_deployments()` -> correlates failure directly with release `v42` deployed 3 minutes ago.
- **Narration**:
  > "FluxWarden autonomously selects diagnostic tools: first checking health metrics, then pulling recent logs to discover an uncaught TypeError, and correlating this with the CI/CD deployment history. It forms the hypothesis: Release v42 introduced the breaking anomaly."

---

### 1:40 – 2:00 | Initial Remediation Strategy: Rollback
- **Visual**: Agent state changes to `PLAN` -> `EXECUTE` with action `rollback_deployment`.
- **Narration**:
  > "Following standard SRE practices, the agent chooses to rollback `payment-api` to previous stable version v41."

---

### 2:00 – 2:15 | The Critical Demonstration: ROLLBACK FAILS
- **Visual**: Timeline step 06 pulses red. Tool result indicates:
  `Rollback failed: Container image for target rollback version 'v41' is unavailable/corrupted in registry.`
- **Narration**:
  > "Here is the key distinction of FluxWarden: The rollback FAILS. In real production, rollbacks often fail due to corrupted images or registry sync issues. A static pipeline or naive script would crash or loop infinitely here."

---

### 2:15 – 2:45 | Agent Detects Failure & Adapts (Replanning)
- **Visual**: State transitions to `REPLAN`. Timeline shows adaptation animation.
- **Observations**:
  - Agent calls `get_backup_status()`
  - Queries Operational Memory for past incident resolutions
  - Discovers standby replica `backup-service` (v40-stable) is 100% healthy and ready for failover.
- **Narration**:
  > "FluxWarden detects the failure, updates its failed actions list, and enters the REPLAN phase. It queries operational memory and inspects service topology, discovering a synchronized standby backup replica."

---

### 2:45 – 3:15 | Adaptive Execution: Traffic Rerouted to Backup
- **Visual**: Agent invokes `route_traffic(target_service="backup-service")`. The live topology graph animates, shifting active ingress traffic lines from `payment-api` to `backup-service`.
- **Narration**:
  > "The agent adapts: instead of futile rollback retries, it invokes `route_traffic`, switching ingress to the healthy backup replica. Notice the live topology graph dynamically updates the traffic path."

---

### 3:15 – 3:40 | Multi-Probe Verification Engine
- **Visual**: Verification phase activates. All 6 verification badges sequentially run:
  1. Service Health & Liveness Probe: PASSED
  2. Synthetic Smoke Test: PASSED (50/50 requests)
  3. Error Rate SLA Check: PASSED (0.001)
  4. Latency SLA Check: PASSED (38ms)
  5. Dependency Health Check: PASSED
  6. Database ACID Integrity Check: PASSED
- **Narration**:
  > "Crucially, FluxWarden does not simply assume success because an API call succeeded. Section 20 of our design requires independent multi-probe verification: health checks, synthetic transactions, latency SLA validation, and database ACID consistency checks."

---

### 3:40 – 4:00 | Final Resolution Card & Forensic Post-Mortem
- **Visual**: Incident Resolved Card appears with celebration glow, displaying Root Cause, Initial Strategy (Failed), Adaptive Recovery (Succeeded), and download buttons for JSON / Markdown reports.
- **Narration**:
  > "All 6 verification checks pass. The incident is formally resolved. FluxWarden compiles a complete post-mortem report and stores the learned resolution in Operational Memory for future incidents. That is genuine agentic AI: Goal, Observe, Decide, Act, Fail, Adapt, Verify, and Recover. Thank you!"
