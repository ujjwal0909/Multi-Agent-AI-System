from app.agents.base import Agent
from app.orchestrator.state import RunState
from app.core.llm import call_llm


class ReasonerAgent(Agent):
    name = "reasoner"

    def run(self, state: RunState) -> None:
        use_rag = state.artifacts.get("use_rag") is True
        evidence_block = ""
        sources = []

        # --- RAG retrieval (safe + low-RAM friendly) ---
        if use_rag:
            try:
                from app.rag.retriever import Retriever

                retriever = Retriever()
                hits = retriever.retrieve(state.user_query, top_k=6)
                sources = hits

                formatted = []
                for i, h in enumerate(hits, start=1):
                    # Limit evidence size so local model stays fast
                    text = h.get("text", "") or ""
                    chunk_preview = (text[:900] + "…") if len(text) > 900 else text

                    formatted.append(
                        f"[S{i}] Source: {h.get('source','?')} (chunk {h.get('chunk_id','?')})\n{chunk_preview}"
                    )
                evidence_block = "\n\n".join(formatted)

            except Exception as e:
                # Don’t crash if index missing / not ingested yet
                state.add(self.name, f"RAG unavailable: {e}", {"rag_error": True})
                sources = []
                evidence_block = ""

        # --- LLM call ---
        system = "You are a careful AI. Use sources if provided. Do NOT invent facts."
        user = f"""
Question:
{state.user_query}

Plan:
{state.artifacts.get("plan","")}

Sources (if any):
{evidence_block}

Rules:
- If sources exist, use them and cite like [S1], [S2].
- If you cannot find support in the sources, say "Not found in documents."
- If no sources, answer generally and say you had no documents.
- Keep it clear and simple.
"""

        answer = call_llm(system, user)

        # Append a short sources list at the bottom (useful even without UI)
        if sources:
            citation_lines = []
            for i, s in enumerate(sources, start=1):
                citation_lines.append(
                    f"[S{i}] {s.get('source','?')} (chunk {s.get('chunk_id','?')})"
                )
            answer = answer + "\n\nSources:\n" + "\n".join(citation_lines)

        state.artifacts["draft_answer"] = answer
        state.artifacts["sources"] = sources
        state.add(self.name, answer, {"sources_used": len(sources)})
