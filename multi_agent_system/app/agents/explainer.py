from app.agents.base import Agent
from app.orchestrator.state import RunState
from app.core.llm import call_llm

class ExplainerAgent(Agent):
    name = "explainer"

    def run(self, state: RunState) -> None:
        system = "You are an AI that explains answers clearly and honestly."
        user = f"""
Question:
{state.user_query}

Draft Answer:
{state.artifacts.get("draft_answer")}

Critique:
{state.artifacts.get("critique")}

Produce a final clear answer.
Also include a short limitations section.
"""

        final_answer = call_llm(system, user)
        confidence = 0.65  # will improve later

        state.artifacts["final_answer"] = final_answer
        state.artifacts["confidence"] = confidence

        state.add(self.name, final_answer, {"confidence": confidence})
