# FluxWarden Agentic Design & State Graph

**Author**: Pochiraju Kailash Ram Markandeya Sharma  
**Team**: kailashsharma8  
**Hackathon**: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar  

FluxWarden embodies genuine agentic behavior: it pursues a goal, observes intermediate results, detects failures, replans alternative strategies, and independently verifies resolution.

---

## The Cognitive Cycle

```
  GOAL
   ↓
 OBSERVE
   ↓
 DECIDE
   ↓
  ACT
   ↓
ACTION FAILS (Intentional Rollback Failure)
   ↓
 ADAPT
   ↓
ACT AGAIN (Reroute Traffic to Standby Backup)
   ↓
 VERIFY (Multi-Probe Verification)
   ↓
RECOVER
```

---

## State Model (`AgentState`)

The state is strongly typed and maintained across turns:

| Field | Type | Description |
| :--- | :--- | :--- |
| `incident_id` | `str` | Unique identifier (e.g. `INC-1042`) |
| `user_goal` | `str` | High-level natural language prompt |
| `constraints` | `list[str]` | Active boundaries (data preservation, no arbitrary commands) |
| `current_phase` | `str` | Current graph node (`INVESTIGATE`, `REPLAN`, etc.) |
| `observations` | `list[str]` | Evidence gathered from telemetry tools |
| `hypotheses` | `list[str]` | Active diagnostic hypotheses |
| `completed_actions` | `list[str]` | Successful tool executions |
| `failed_actions` | `list[dict]` | Errors encountered during remediation |
| `tool_results` | `list[dict]` | Full payload history of tool outputs |
| `system_state` | `dict` | Snapshot of microservice health and traffic targets |
| `risk_level` | `str` | Current risk classification (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`) |
| `approval_required`| `bool` | Flag pausing execution until operator confirms |
| `attempt_count` | `int` | Bounded step counter (capped at `MAX_AGENT_STEPS = 15`) |
| `replan_count` | `int` | Replanning counter (capped at `MAX_REPLAN_ATTEMPTS = 3`) |
| `resolution_status`| `str` | Status (`UNRESOLVED`, `INVESTIGATING`, `RESOLVED`, etc.) |
| `final_report` | `dict` | Complete post-mortem exportable as JSON/Markdown |

---

## Safe Agent Explanations (No Raw CoT Leaks)

FluxWarden never exposes raw LLM internal chains of thought to the UI. Instead, every action is structured into an operational summary:

- **CURRENT ACTION**: Precise tool invocation
- **WHY**: Operational rationale correlated with telemetry
- **EXPECTED RESULT**: Quantitative SLA recovery expectation
- **RISK**: Evaluated impact level
- **RESULT**: Concrete outcome from execution
- **ADAPTATION**: Rationale for changing course upon failure
