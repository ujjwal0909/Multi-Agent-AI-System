import sqlite3
from pathlib import Path
from typing import Dict, Any, List
import json

DB_PATH = Path("data/runs.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def _conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    with _conn() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            created_at TEXT,
            user_query TEXT,
            use_rag INTEGER,
            strict INTEGER,
            confidence REAL,
            final_answer TEXT,
            sources_json TEXT,
            trace_json TEXT
        )
        """)
        c.commit()

def save_run(run: Dict[str, Any]) -> None:
    init_db()
    with _conn() as c:
        c.execute("""
        INSERT OR REPLACE INTO runs
        (run_id, created_at, user_query, use_rag, strict, confidence, final_answer, sources_json, trace_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run["run_id"],
            run.get("created_at"),
            run.get("user_query"),
            1 if run.get("use_rag") else 0,
            1 if run.get("strict") else 0,
            float(run.get("confidence", 0.0)),
            run.get("final_answer", ""),
            json.dumps(run.get("sources", []), ensure_ascii=False),
            json.dumps(run.get("trace", []), ensure_ascii=False),
        ))
        c.commit()

def load_run(run_id: str) -> Dict[str, Any]:
    init_db()
    with _conn() as c:
        row = c.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        if not row:
            raise FileNotFoundError(f"Run not found: {run_id}")

        cols = [d[0] for d in c.execute("PRAGMA table_info(runs)").fetchall()]
        data = dict(zip(cols, row))
        return _hydrate(data)

def list_runs(limit: int = 50) -> List[Dict[str, Any]]:
    init_db()
    with _conn() as c:
        rows = c.execute(
            "SELECT run_id, created_at, user_query, use_rag, strict, confidence, final_answer FROM runs ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()

    out = []
    for run_id, created_at, user_query, use_rag, strict, confidence, final_answer in rows:
        q = user_query or ""
        ans = final_answer or ""
        out.append({
            "run_id": run_id,
            "created_at": created_at,
            "confidence": confidence,
            "use_rag": bool(use_rag),
            "strict": bool(strict),
            "query_preview": (q[:90] + "...") if len(q) > 90 else q,
            "final_answer_preview": (ans[:140] + "...") if len(ans) > 140 else ans,
        })
    return out

def search_runs(query: str, limit: int = 50) -> List[Dict[str, Any]]:
    init_db()
    q = (query or "").strip()
    like = f"%{q}%"

    with _conn() as c:
        rows = c.execute(
            """SELECT run_id, created_at, user_query, use_rag, strict, confidence, final_answer
               FROM runs
               WHERE user_query LIKE ? OR final_answer LIKE ?
               ORDER BY created_at DESC
               LIMIT ?""",
            (like, like, limit)
        ).fetchall()

    out = []
    for run_id, created_at, user_query, use_rag, strict, confidence, final_answer in rows:
        uq = user_query or ""
        ans = final_answer or ""
        out.append({
            "run_id": run_id,
            "created_at": created_at,
            "confidence": confidence,
            "use_rag": bool(use_rag),
            "strict": bool(strict),
            "query_preview": (uq[:90] + "...") if len(uq) > 90 else uq,
            "final_answer_preview": (ans[:140] + "...") if len(ans) > 140 else ans,
        })
    return out

def delete_run(run_id: str) -> None:
    init_db()
    with _conn() as c:
        c.execute("DELETE FROM runs WHERE run_id = ?", (run_id,))
        c.commit()

def export_all() -> List[Dict[str, Any]]:
    init_db()
    with _conn() as c:
        rows = c.execute("SELECT * FROM runs ORDER BY created_at DESC").fetchall()
        cols = [d[0] for d in c.execute("PRAGMA table_info(runs)").fetchall()]
    return [_hydrate(dict(zip(cols, r))) for r in rows]

def _hydrate(data: Dict[str, Any]) -> Dict[str, Any]:
    # Convert sqlite row dict to expected API output
    return {
        "run_id": data["run_id"],
        "created_at": data["created_at"],
        "user_query": data["user_query"],
        "use_rag": bool(data["use_rag"]),
        "strict": bool(data["strict"]),
        "confidence": float(data["confidence"]),
        "final_answer": data["final_answer"],
        "sources": json.loads(data["sources_json"] or "[]"),
        "trace": json.loads(data["trace_json"] or "[]"),
    }
