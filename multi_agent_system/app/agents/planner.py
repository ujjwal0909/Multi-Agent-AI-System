from app.agents.base import Agent
from app.orchestrator.state import RunState
from app.core.llm import call_llm

class PlannerAgent(Agent):
    name = "planner"

    def run(self, state: RunState) -> None:
        system = "You are a planner AI that breaks questions into steps."
        user = f"""
User question:
{state.user_query}

Return a clear step-by-step plan.
"""

        plan_text = call_llm(system, user)
        state.artifacts["plan"] = plan_text

        state.add(self.name, plan_text)
