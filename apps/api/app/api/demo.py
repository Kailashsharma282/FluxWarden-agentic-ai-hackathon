import asyncio
from fastapi import APIRouter, BackgroundTasks
from app.agents.engine import agent_engine
from app.simulations.environment import sim_env

router = APIRouter(prefix="/api/demo", tags=["demo"])

async def execute_demo_sequence(step_delay: float = 1.0):
    # 1. Reset environment
    sim_env.reset_environment()
    await asyncio.sleep(0.5)

    # 2. Inject bad deployment
    sim_env.inject_scenario("bad_deployment")
    await asyncio.sleep(0.8)

    # 3. Initialize mission
    goal = "The payment API is failing. Investigate the cause and restore service without causing data loss."
    await agent_engine.initialize_mission(user_goal=goal, incident_id="INC-1042")

    # 4. Run autonomous loop (it will investigate -> attempt rollback -> rollback fails intentionally -> replan -> discover backup -> route traffic -> verify -> resolve!)
    await agent_engine.run_mission_loop(delay=step_delay)

@router.post("/run")
async def run_demo(background_tasks: BackgroundTasks, step_delay: float = 0.9):
    # Launch background autonomous execution
    background_tasks.add_task(execute_demo_sequence, step_delay=step_delay)
    return {
        "status": "demo_initiated",
        "scenario": "bad_deployment",
        "description": "Running deterministic demo sequence: Goal -> Investigate -> Rollback -> Intentional Fail -> Replan -> Backup Route -> Multi-Check Verify -> Recover."
    }
