import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("fluxwarden.llm")

class LLMActionPlan(BaseModel):
    phase: str
    thought_summary: str
    current_action: str
    why: str
    expected_result: str
    risk: str = "LOW"
    adaptation_reason: str = ""
    tool_to_execute: Optional[str] = None
    tool_parameters: dict[str, Any] = Field(default_factory=dict)
    hypotheses: list[str] = Field(default_factory=list)
    is_terminal: bool = False
    resolution_status: Optional[str] = None

class BaseLLMProvider(ABC):
    @abstractmethod
    async def decide_next_step(self, context: dict[str, Any]) -> LLMActionPlan:
        pass

class MockLLMProvider(BaseLLMProvider):
    """
    Autonomous Mock Provider (Default).
    Executes the authentic Goal -> Observe -> Decide -> Act -> Evaluate -> Re-plan -> Verify cognitive sequence
    without requiring external paid API keys.
    """
    async def decide_next_step(self, context: dict[str, Any]) -> LLMActionPlan:
        current_phase = context.get("current_phase", "IDLE")
        observations = context.get("observations", [])
        completed_actions = context.get("completed_actions", [])
        failed_actions = context.get("failed_actions", [])
        attempt_count = context.get("attempt_count", 0)
        scenario = context.get("scenario", "bad_deployment")

        # Phase 1 & 2: Understood Goal -> Begin Investigation
        if current_phase in ["IDLE", "UNDERSTAND_GOAL", "INVESTIGATE"]:
            if "get_service_health" not in completed_actions:
                return LLMActionPlan(
                    phase="INVESTIGATE",
                    thought_summary="Incident goal received. Commencing initial service health discovery and telemetry scan.",
                    current_action="Query service health",
                    why="Determine primary failure blast radius and current error rate across payment cluster.",
                    expected_result="Confirm whether payment-api is responding with 5xx status codes.",
                    risk="LOW",
                    tool_to_execute="get_service_health",
                    tool_parameters={"service_name": "payment-api"},
                    hypotheses=["Payment API is experiencing active service degradation"]
                )
            elif "get_recent_logs" not in completed_actions:
                return LLMActionPlan(
                    phase="INVESTIGATE",
                    thought_summary="High error rate observed (0.74). Inspecting recent stderr/stdout logs for error signatures.",
                    current_action="Inspect recent service logs",
                    why="Identify stack traces and specific error signatures causing request drops.",
                    expected_result="Locate specific runtime exceptions or database disconnects.",
                    risk="LOW",
                    tool_to_execute="get_recent_logs",
                    tool_parameters={"service_name": "payment-api", "limit": 10},
                    hypotheses=["Unhandled application exception in latest release"]
                )
            elif "get_recent_deployments" not in completed_actions:
                return LLMActionPlan(
                    phase="HYPOTHESIS",
                    thought_summary="Logs indicate NullPointerReference in PaymentGateway.processTransaction. Correlating with deployment history.",
                    current_action="Inspect deployment history",
                    why="Check if recent code deployment correlate with latency/error spike.",
                    expected_result="Identify deployment timestamp, release version, and commit author.",
                    risk="LOW",
                    tool_to_execute="get_recent_deployments",
                    tool_parameters={"service_name": "payment-api"},
                    hypotheses=["Bad deployment v42 introduced breaking change"]
                )

        # Phase 3: Formulate hypothesis and plan initial strategy
        if current_phase == "HYPOTHESIS":
            if scenario == "bad_deployment":
                return LLMActionPlan(
                    phase="PLAN",
                    thought_summary="Correlated spike directly to version v42 deployment. Initiating rollback to previous stable version v41.",
                    current_action="Rollback deployment",
                    why="Recent deployment correlates directly with 74% error rate and fatal exceptions.",
                    expected_result="Return payment-api to previous stable version v41.",
                    risk="MEDIUM",
                    tool_to_execute="rollback_deployment",
                    tool_parameters={"service_name": "payment-api"},
                    hypotheses=["Rollback to v41 will eliminate NullPointerReference"]
                )
            elif scenario == "db_connection_exhaustion":
                return LLMActionPlan(
                    phase="PLAN",
                    thought_summary="Postgres pool exhausted (498/500). Scaling connection pool and restarting stalled workers.",
                    current_action="Scale service pool",
                    why="Application connection pool reached saturation limit.",
                    expected_result="Reset connection pool and allocate additional replica headroom.",
                    risk="MEDIUM",
                    tool_to_execute="scale_service",
                    tool_parameters={"service_name": "payment-api", "replicas": 3},
                    hypotheses=["Increasing pool headroom clears thread queue"]
                )
            elif scenario == "redis_outage":
                return LLMActionPlan(
                    phase="PLAN",
                    thought_summary="Redis cache unreachable. Executing failover to standby Redis node.",
                    current_action="Failover Redis cache",
                    why="Primary Redis instance crashed with OOM.",
                    expected_result="Promote standby Redis instance to primary.",
                    risk="HIGH",
                    tool_to_execute="failover_service",
                    tool_parameters={"service_name": "redis"},
                    hypotheses=["Hot standby failover restores instant caching"]
                )

        # Phase 4: Execute & Evaluate
        if current_phase in ["PLAN", "EXECUTE"]:
            has_failed_rollback = any(f.get("tool") == "rollback_deployment" for f in failed_actions)
            if has_failed_rollback and "get_backup_status" in completed_actions and "route_traffic" not in completed_actions:
                return LLMActionPlan(
                    phase="EXECUTE",
                    thought_summary="Standby replica is healthy (score: 100). Executing adaptive failover: Reroute 100% traffic to backup-service.",
                    current_action="Reroute ingress traffic to backup-service",
                    why="Primary payment API rollback is impossible. Rerouting traffic to healthy standby replica restores service immediately.",
                    expected_result="Global ingress traffic flows to healthy backup-service.",
                    risk="MEDIUM",
                    adaptation_reason="Adaptive Recovery: Routing around corrupted primary deployment via healthy standby replica.",
                    tool_to_execute="route_traffic",
                    tool_parameters={"target_service": "backup-service"},
                    hypotheses=["Routing to backup-service resolves user facing errors"]
                )

            # If rollback was selected, transition to EXECUTE
            action = context.get("selected_action", "rollback_deployment")
            return LLMActionPlan(
                phase="EXECUTE",
                thought_summary=f"Executing planned remediation: {action}.",
                current_action=f"Execute {action}",
                why="Apply remediation strategy to restore SLA.",
                expected_result="Verify immediate recovery or failure state.",
                risk="MEDIUM",
                tool_to_execute=action,
                tool_parameters={"service_name": "payment-api"}
            )

        # Phase 5: Failure detected! -> REPLAN (Central showcase of adaptation!)
        if current_phase in ["EVALUATE", "REPLAN"]:
            # If an action failed (e.g. rollback_deployment failed due to missing image)
            has_failed_rollback = any(f.get("tool") == "rollback_deployment" for f in failed_actions)

            if has_failed_rollback and "route_traffic" not in completed_actions:
                # Step A in Replanning: Check Operational Memory and Backup Status
                if "get_backup_status" not in completed_actions:
                    return LLMActionPlan(
                        phase="REPLAN",
                        thought_summary="ACTION FAILED: Rollback failed because previous image manifest is corrupted/unavailable. Querying Operational Memory & topology for alternate recovery paths.",
                        current_action="Inspect standby backup service status",
                        why="Rollback aborted. Checking if standby payment replica is available and healthy.",
                        expected_result="Confirm standby backup-service (v40-stable) is synchronized and ready for traffic.",
                        risk="LOW",
                        adaptation_reason="Rollback failed (image unavailable). Adapting strategy from rollback to live traffic failover.",
                        tool_to_execute="get_backup_status",
                        tool_parameters={},
                        hypotheses=["Standby replica backup-service can absorb 100% production traffic without downtime"]
                    )
                else:
                    # Step B in Replanning: Reroute traffic to backup service!
                    return LLMActionPlan(
                        phase="EXECUTE",
                        thought_summary="Standby replica is healthy (score: 100). Executing adaptive failover: Reroute 100% traffic to backup-service.",
                        current_action="Reroute ingress traffic to backup-service",
                        why="Primary payment API rollback is impossible. Rerouting traffic to healthy standby replica restores service immediately.",
                        expected_result="Global ingress traffic flows to healthy backup-service.",
                        risk="MEDIUM",
                        adaptation_reason="Adaptive Recovery: Routing around corrupted primary deployment via healthy standby replica.",
                        tool_to_execute="route_traffic",
                        tool_parameters={"target_service": "backup-service"},
                        hypotheses=["Routing to backup-service resolves user facing errors"]
                    )

        # Phase 6: Verification
        if current_phase == "VERIFY":
            return LLMActionPlan(
                phase="VERIFY",
                thought_summary="Remediation applied. Initiating independent multi-check verification suite.",
                current_action="Run independent verification suite",
                why="Section 20: Success response alone does NOT resolve incident. Must independently verify health, latency, error rate, and DB integrity.",
                expected_result="Confirm all 6 verification checks pass.",
                risk="LOW",
                tool_to_execute="verify_service_recovery",
                tool_parameters={}
            )

        # Default fallback
        return LLMActionPlan(
            phase="COMPLETE",
            thought_summary="All verification checks passed. Incident resolved autonomously.",
            current_action="Finalize incident report",
            why="Service SLA restored and verified.",
            expected_result="Complete incident lifecycle.",
            risk="LOW",
            is_terminal=True,
            resolution_status="RESOLVED",
            tool_to_execute="create_incident_report",
            tool_parameters={"incident_id": context.get("incident_id", "INC-CURRENT")}
        )

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def decide_next_step(self, context: dict[str, Any]) -> LLMActionPlan:
        # Fallback to Mock provider logic if key not configured, or if API fails
        if not self.api_key:
            return await MockLLMProvider().decide_next_step(context)
        try:
            # When OpenAI key is present, can invoke OpenAI REST API via httpx
            import httpx
            prompt = f"You are FluxWarden autonomous incident agent. State: {json.dumps(context)}. Return JSON matching LLMActionPlan schema."
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": "gpt-4o",
                        "messages": [{"role": "system", "content": "You are FluxWarden SRE AI."}, {"role": "user", "content": prompt}],
                        "response_format": {"type": "json_object"}
                    }
                )
                if res.status_code == 200:
                    data = res.json()["choices"][0]["message"]["content"]
                    return LLMActionPlan.model_validate_json(data)
        except Exception as e:
            logger.warning(f"OpenAI call failed, gracefully falling back to resilient state engine: {e}")
        return await MockLLMProvider().decide_next_step(context)

class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def decide_next_step(self, context: dict[str, Any]) -> LLMActionPlan:
        if not self.api_key:
            return await MockLLMProvider().decide_next_step(context)
        try:
            import httpx
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            prompt = (
                f"You are FluxWarden autonomous SRE agent. Context: {json.dumps(context)}.\n"
                "Return a JSON object conforming to this schema:\n"
                "{\n"
                '  "phase": "INVESTIGATE"|"PLAN"|"EXECUTE"|"REPLAN"|"VERIFY"|"COMPLETE",\n'
                '  "thought_summary": string,\n'
                '  "current_action": string,\n'
                '  "why": string,\n'
                '  "expected_result": string,\n'
                '  "risk": "LOW"|"MEDIUM"|"HIGH"|"CRITICAL",\n'
                '  "adaptation_reason": string,\n'
                '  "tool_to_execute": string|null,\n'
                '  "tool_parameters": object,\n'
                '  "hypotheses": [string],\n'
                '  "is_terminal": boolean,\n'
                '  "resolution_status": string|null\n'
                "}"
            )
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"response_mime_type": "application/json"}
                    }
                )
                if res.status_code == 200:
                    text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                    json_str = text[text.find("{"):text.rfind("}")+1]
                    return LLMActionPlan.model_validate_json(json_str)
        except Exception as e:
            logger.warning(f"Gemini API call failed, falling back to resilient state engine: {e}")
        return await MockLLMProvider().decide_next_step(context)

class AnthropicProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def decide_next_step(self, context: dict[str, Any]) -> LLMActionPlan:
        if not self.api_key:
            return await MockLLMProvider().decide_next_step(context)
        try:
            import httpx
            prompt = f"Context: {json.dumps(context)}. Output JSON matching LLMActionPlan."
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"x-api-key": self.api_key, "anthropic-version": "2023-06-01"},
                    json={
                        "model": "claude-3-5-sonnet-20240620",
                        "max_tokens": 1024,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                if res.status_code == 200:
                    text = res.json()["content"][0]["text"]
                    json_str = text[text.find("{"):text.rfind("}")+1]
                    return LLMActionPlan.model_validate_json(json_str)
        except Exception as e:
            logger.warning(f"Anthropic API call failed, falling back to resilient engine: {e}")
        return await MockLLMProvider().decide_next_step(context)

def get_llm_provider(provider_name: str, settings: Any) -> BaseLLMProvider:
    provider = provider_name.lower()
    if provider == "openai" and settings.OPENAI_API_KEY:
        return OpenAIProvider(settings.OPENAI_API_KEY)
    elif provider == "gemini" and settings.GEMINI_API_KEY:
        return GeminiProvider(settings.GEMINI_API_KEY)
    elif provider == "anthropic" and settings.ANTHROPIC_API_KEY:
        return AnthropicProvider(settings.ANTHROPIC_API_KEY)
    return MockLLMProvider()
