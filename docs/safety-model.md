# FluxWarden Safety & Governance Model

**Author**: Pochiraju Kailash Ram Markandeya Sharma  
**Team**: kailashsharma8  
**Hackathon**: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar  

FluxWarden implements enterprise safety guardrails to ensure autonomous actions never endanger real production infrastructure or violate security boundaries.

---

## 1. Action Risk Hierarchy

Every tool in the system is evaluated by the **Risk Engine** before execution:

```
┌────────────────────────────────────────────────────────┐
│                        CRITICAL                        │
│ (Drop database, delete persistent state) - STRICTLY    │
│ BLOCKED from autonomous execution                      │
├────────────────────────────────────────────────────────┤
│                          HIGH                          │
│ (Failover cluster, restore backup snapshot) - REQUIRES │
│ HUMAN OPERATOR APPROVAL MODAL                          │
├────────────────────────────────────────────────────────┤
│                         MEDIUM                         │
│ (Reroute traffic, scale replicas, rollback image) -    │
│ MONITORED AUTONOMOUS EXECUTION                         │
├────────────────────────────────────────────────────────┤
│                          LOW                           │
│ (Inspect metrics, read logs, check health, warm cache) │
│ - SAFE AUTONOMOUS EXECUTION                            │
└────────────────────────────────────────────────────────┘
```

---

## 2. Human-in-the-Loop Approval Workflow

When the agent plans an action categorized as `HIGH` or `CRITICAL`:

1. The agent state pauses and transitions to `WAITING_FOR_APPROVAL`.
2. An interactive **Human Approval Modal** renders on the UI displaying:
   - **Action**: Proposed tool and parameters
   - **Impact**: Potential consequences to system state
   - **Reason**: Rationale why this action is required
   - **Safety**: Verification safeguards that will execute afterward
3. The operator can choose:
   - **Approve**: Resumes execution, runs the approved tool, and emits `ACTION_STARTED`.
   - **Reject**: Cancels the action, sets state to `REPLAN`, and forces the agent to explore alternate paths.

---

## 3. Sandboxed Execution

- All tools operate strictly within the **Simulation Environment**.
- Arbitrary host shell commands, raw Bash subprocess execution, and system-level root access are strictly forbidden.
- Tool arguments are validated against strict Pydantic schemas.

---

## 4. Loop Bounding & Infinite Cycle Prevention

To prevent runaway autonomy or hallucination loops:
- `MAX_AGENT_STEPS = 15`: Hard ceiling on autonomous steps per incident.
- `MAX_REPLAN_ATTEMPTS = 3`: Maximum number of replanning attempts before safe escalation.
- `MAX_TOOL_RETRIES = 2`: Maximum retries on individual tool errors.
- If boundaries are exceeded, the agent halts safely, transitions to `FAILED`/`ESCALATED`, pages human on-call engineers, and never crashes.
