from enum import Enum
from typing import Optional

class AgentStatePhase(str, Enum):
    IDLE = "IDLE"
    UNDERSTAND_GOAL = "UNDERSTAND_GOAL"
    INVESTIGATE = "INVESTIGATE"
    HYPOTHESIS = "HYPOTHESIS"
    PLAN = "PLAN"
    EXECUTE = "EXECUTE"
    EVALUATE = "EVALUATE"
    REPLAN = "REPLAN"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    VERIFY = "VERIFY"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"

class StateTransitionEngine:
    """
    Explicit finite state machine enforcing strict transitions.
    Prevents uncontrolled autonomous infinite loops.
    """
    VALID_TRANSITIONS = {
        AgentStatePhase.IDLE: [AgentStatePhase.UNDERSTAND_GOAL],
        AgentStatePhase.UNDERSTAND_GOAL: [AgentStatePhase.INVESTIGATE, AgentStatePhase.FAILED],
        AgentStatePhase.INVESTIGATE: [AgentStatePhase.INVESTIGATE, AgentStatePhase.HYPOTHESIS, AgentStatePhase.FAILED],
        AgentStatePhase.HYPOTHESIS: [AgentStatePhase.PLAN, AgentStatePhase.INVESTIGATE, AgentStatePhase.FAILED],
        AgentStatePhase.PLAN: [AgentStatePhase.EXECUTE, AgentStatePhase.WAITING_FOR_APPROVAL, AgentStatePhase.FAILED],
        AgentStatePhase.WAITING_FOR_APPROVAL: [AgentStatePhase.EXECUTE, AgentStatePhase.REPLAN, AgentStatePhase.FAILED],
        AgentStatePhase.EXECUTE: [AgentStatePhase.EVALUATE, AgentStatePhase.FAILED],
        AgentStatePhase.EVALUATE: [AgentStatePhase.VERIFY, AgentStatePhase.REPLAN, AgentStatePhase.FAILED],
        AgentStatePhase.REPLAN: [AgentStatePhase.INVESTIGATE, AgentStatePhase.PLAN, AgentStatePhase.EXECUTE, AgentStatePhase.FAILED],
        AgentStatePhase.VERIFY: [AgentStatePhase.COMPLETE, AgentStatePhase.REPLAN, AgentStatePhase.FAILED],
        AgentStatePhase.COMPLETE: [AgentStatePhase.IDLE],
        AgentStatePhase.FAILED: [AgentStatePhase.IDLE]
    }

    @classmethod
    def can_transition(cls, from_phase: str, to_phase: str) -> bool:
        try:
            current = AgentStatePhase(from_phase)
            target = AgentStatePhase(to_phase)
            return target in cls.VALID_TRANSITIONS.get(current, [])
        except ValueError:
            return False
