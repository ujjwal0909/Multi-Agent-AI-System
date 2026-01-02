from fastapi import APIRouter
from app.api.schemas import QueryRequest, QueryResponse
from app.orchestrator.runner import run_pipeline
from app.core.run_store_sqlite import list_runs, load_run, search_runs, delete_run, export_all

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    return run_pipeline(req.query, use_rag=req.use_rag, strict=req.strict)
@router.get("/runs")
def runs():
    return list_runs(limit=50)

@router.get("/runs/{run_id}")
def run_detail(run_id: str):
    return load_run(run_id)
from fastapi import APIRouter
from app.api.schemas import QueryRequest, QueryResponse
from app.orchestrator.runner import run_pipeline
from app.core.run_store import list_runs, load_run, search_runs

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    return run_pipeline(req.query, use_rag=req.use_rag, strict=req.strict)

@router.get("/runs")
def runs():
    return list_runs(limit=50)

@router.get("/runs/search")
def runs_search(q: str):
    return search_runs(q, limit=50)

@router.get("/runs/{run_id}")
def run_detail(run_id: str):
    return load_run(run_id)
@router.delete("/runs/{run_id}")
def delete_run_api(run_id: str):
    delete_run(run_id)
    return {"ok": True}

@router.get("/runs/export/all")
def export_all_api():
    return export_all()
