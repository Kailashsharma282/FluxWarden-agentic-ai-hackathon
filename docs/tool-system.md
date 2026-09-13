# FluxWarden Tool Registry System

**Author**: Pochiraju Kailash Ram Markandeya Sharma  
**Team**: kailashsharma8  
**Hackathon**: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar  

FluxWarden implements a dedicated Tool Registry providing 39 tools across 4 operational categories. All tools execute strictly within the simulated production sandbox—never allowing arbitrary host shell commands.

---

## 1. Diagnostic Tools (17 Tools)

1. `get_service_status`: Check health status and active release version.
2. `get_service_health`: Retrieve comprehensive telemetry metrics and health score.
3. `get_recent_logs`: Query recent stdout/stderr log entries for a service.
4. `search_logs`: Full-text grep search across infrastructure logs.
5. `get_metrics`: Read CPU, memory, error rate, and latency metrics.
6. `get_error_rate`: Extract HTTP 5xx/4xx error percentage.
7. `get_latency`: Extract p95/p99 latency in milliseconds.
8. `get_cpu_usage`: Read container CPU core allocation.
9. `get_memory_usage`: Read container RAM consumption.
10. `get_database_health`: Inspect Postgres connection pool and query engine.
11. `get_redis_health`: Inspect Redis memory and key eviction state.
12. `get_dependency_status`: Check upstream and downstream service dependencies.
13. `get_recent_deployments`: Inspect CI/CD release history, commit hashes, and container manifests.
14. `get_current_configuration`: Inspect active environment variables and timeouts.
15. `inspect_network`: Examine network routing, gateway health, and packet drops.
16. `get_backup_status`: Check standby replica synchronization and health.
17. `get_traffic_distribution`: Query load balancer ingress split percentages.

---

## 2. Remediation Tools (9 Tools)

1. `restart_service` (Risk: LOW): Gracefully restart a container instance.
2. `rollback_deployment` (Risk: MEDIUM): Rollback service to previous container release. *(Fails intentionally in Scenario A when image manifest is unavailable)*.
3. `restore_configuration` (Risk: MEDIUM): Reset service configuration to known baseline.
4. `route_traffic` (Risk: MEDIUM): Reroute ingress traffic to standby or alternate services.
5. `scale_service` (Risk: MEDIUM): Dynamically scale worker container replicas.
6. `clear_cache` (Risk: LOW): Flush corrupted cache keys from Redis.
7. `failover_service` (Risk: HIGH): Promote standby replica to active primary cluster.
8. `restore_backup` (Risk: HIGH): Restore persistent database snapshot.
9. `disable_dependency` (Risk: MEDIUM): Isolate failing external dependency with circuit breaker.

---

## 3. Verification Tools (9 Tools)

1. `run_health_check`: HTTP liveness & readiness probes.
2. `run_smoke_test`: Synthetic multi-endpoint API test suite.
3. `run_payment_test`: Synthetic end-to-end checkout transactions.
4. `check_error_rate`: Confirm error rate is under 5% SLA threshold.
5. `check_latency`: Confirm response latency is under 200ms threshold.
6. `check_dependency_health`: Verify all downstream dependencies are responsive.
7. `verify_database_integrity`: Verify ACID transaction integrity and connection pool headroom.
8. `verify_traffic_distribution`: Validate ingress traffic routing accuracy.
9. `verify_service_recovery`: Holistic multi-probe verification confirming recovery.

---

## 4. Safety Tools (4 Tools)

1. `request_human_approval`: Request human confirmation for HIGH/CRITICAL actions.
2. `create_incident_report`: Compile structured post-mortem artifact.
3. `escalate_incident`: Page on-call human engineering responders.
4. `close_incident`: Formally mark incident resolved in database.
