from app.agents.base import Agent
from app.orchestrator.state import RunState
from app.core.llm import call_llm

class CriticAgent(Agent):
    name = "critic"

    def run(self, state: RunState) -> None:
        system = "You are a strict reviewer. Be brief and practical."
        user = f"""
Question:
{state.user_query}

Answer:
{state.artifacts.get("draft_answer","")}

Task:
- List up to 5 issues max (missing facts, unclear parts, possible hallucinations).
- If sources exist, check if answer matches them.
- Output as bullet points.
"""
        critique = call_llm(system, user)
        state.artifacts["critique"] = critique

        # Append critic notes to final answer
        state.artifacts["draft_answer"] = state.artifacts.get("draft_answer","") + "\n\nCritic Notes:\n" + critique
        state.add(self.name, critique)
