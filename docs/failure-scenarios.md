# FluxWarden Failure Scenarios & Chaos Lab

**Author**: Pochiraju Kailash Ram Markandeya Sharma  
**Team**: kailashsharma8  
**Hackathon**: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar  

FluxWarden features a realistic Chaos Simulation Engine capable of injecting 6 distinct infrastructure incidents into the simulated 10-node production cluster.

---

## Scenario Catalog

### Scenario A — Bad Deployment (Primary Adaptation Showcase)
- **Severity**: CRITICAL
- **Injected Anomaly**: Release `v42` deployed to `payment-api` with unhandled schema panic in `PaymentGateway.processTransaction()`.
- **Symptoms**:
  - HTTP 500 error rate spikes to 74%
  - Latency surges to 921ms
  - Logs show fatal `NullPointerReference`
- **Initial Agent Strategy**: Investigate logs, identify `dep-42`, attempt `rollback_deployment`.
- **Intentionally Forced Failure**: Rollback fails because previous image manifest `v41` is missing/corrupted in the deployment registry (SHA256 mismatch).
- **Adaptive Recovery**:
  - Agent detects rollback failure without crashing
  - Enters `REPLAN` state
  - Discovers standby healthy replica `backup-service` (v40-stable, error rate 0.001, latency 38ms)
  - Executes `route_traffic` to redirect global ingress to `backup-service`
  - Runs independent 6-probe verification suite
  - Confirms recovery and compiles forensic report.

---

### Scenario B — Database Connection Exhaustion
- **Severity**: HIGH
- **Injected Anomaly**: PostgreSQL active connection pool saturated at 498/500 threads.
- **Symptoms**: Application thread lockup, `ConnectionPoolTimeout` errors, queries hanging.
- **Remediation**: Scale connection pool headroom (`scale_service`), reset stalled connection pools.

---

### Scenario C — Redis Cache Failure
- **Severity**: HIGH
- **Injected Anomaly**: Redis container process crashes during keyspace scan (OOM).
- **Symptoms**: Port 6379 connection refused, un-cached database thrashing, latency degradation.
- **Remediation**: Failover to standby Redis node (`failover_service`), warm active cache keys.

---

### Scenario D — Payment API Memory Leak
- **Severity**: MEDIUM
- **Injected Anomaly**: Progressive heap allocation leak in `payment-api` reaching 96% RAM.
- **Symptoms**: JVM garbage collection pauses (420ms), degraded throughput.
- **Remediation**: Graceful worker restart (`restart_service`) and dynamic container memory scaling.

---

### Scenario E — Third-Party Dependency Latency
- **Severity**: MEDIUM
- **Injected Anomaly**: Upstream external fraud verification service responds with 2500ms delay.
- **Symptoms**: Client checkout requests timing out.
- **Remediation**: Activate circuit breaker (`disable_dependency`) and enable graceful fallback.

---

### Scenario F — Ingress Network Latency
- **Severity**: MEDIUM
- **Injected Anomaly**: Ingress gateway packet jitter on traffic router reaching 850ms.
- **Symptoms**: Overall cluster latency elevated.
- **Remediation**: Inspect network routes and flush stale gateway ingress rules.
