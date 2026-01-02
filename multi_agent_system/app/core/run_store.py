import json
from pathlib import Path
from typing import Dict, Any, List

RUNS_DIR = Path("data/runs")
RUNS_DIR.mkdir(parents=True, exist_ok=True)

def save_run(run: Dict[str, Any]) -> None:
    run_id = run["run_id"]
    path = RUNS_DIR / f"{run_id}.json"
    path.write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")

def load_run(run_id: str) -> Dict[str, Any]:
    path = RUNS_DIR / f"{run_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Run not found: {run_id}")
    return json.loads(path.read_text(encoding="utf-8"))

def list_runs(limit: int = 50) -> List[Dict[str, Any]]:
    files = sorted(RUNS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    runs = []
    for f in files[:limit]:
        data = json.loads(f.read_text(encoding="utf-8"))
        q = data.get("user_query", "")
        ans = data.get("final_answer", "")
        runs.append({
            "run_id": data.get("run_id"),
            "created_at": data.get("created_at"),
            "confidence": data.get("confidence"),
            "use_rag": data.get("use_rag", False),
            "strict": data.get("strict", False),
            "query_preview": (q[:90] + "...") if len(q) > 90 else q,
            "final_answer_preview": (ans[:140] + "...") if len(ans) > 140 else ans,
        })
    return runs

def search_runs(query: str, limit: int = 50) -> List[Dict[str, Any]]:
    files = sorted(RUNS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    out: List[Dict[str, Any]] = []
    q = (query or "").lower().strip()

    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        hay = (data.get("user_query", "") + "\n" + data.get("final_answer", "")).lower()
        if q in hay:
            user_q = data.get("user_query", "")
            ans = data.get("final_answer", "")
            out.append({
                "run_id": data.get("run_id"),
                "created_at": data.get("created_at"),
                "confidence": data.get("confidence"),
                "use_rag": data.get("use_rag", False),
                "strict": data.get("strict", False),
                "query_preview": (user_q[:90] + "...") if len(user_q) > 90 else user_q,
                "final_answer_preview": (ans[:140] + "...") if len(ans) > 140 else ans,
            })

        if len(out) >= limit:
            break

    return out
