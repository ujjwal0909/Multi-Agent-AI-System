from datetime import datetime, timezone
from app.orchestrator.state import RunState
from app.agents.planner import PlannerAgent
from app.agents.reasoner import ReasonerAgent
from app.agents.critic import CriticAgent
from app.core.run_store_sqlite import save_run


def run_pipeline(user_query: str, use_rag: bool = False, strict: bool = False):
    state = RunState(user_query=user_query)
    state.artifacts["use_rag"] = use_rag
    state.artifacts["strict"] = strict

    # FAST MODE: 2 agents always
    for agent in [PlannerAgent(), ReasonerAgent()]:
        agent.run(state)

    # Simple confidence heuristic
    sources = state.artifacts.get("sources", [])
    if use_rag and sources:
        confidence = min(0.9, 0.5 + 0.1 * len(sources))
    else:
        confidence = 0.45

    # OPTIONAL critic: strict OR low confidence
    if strict or confidence < 0.6:
        CriticAgent().run(state)
        confidence = max(0.2, confidence - 0.1)

    state.artifacts["final_answer"] = state.artifacts.get("draft_answer", "")
    state.artifacts["confidence"] = round(confidence, 2)

    result = {
        "run_id": state.run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "user_query": user_query,
        "use_rag": use_rag,
        "strict": strict,
        "final_answer": state.artifacts["final_answer"],
        "confidence": state.artifacts["confidence"],
        "sources": state.artifacts.get("sources", []),
        "trace": state.trace,
    }

    save_run(result)
    return result
