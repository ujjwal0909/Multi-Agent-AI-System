from pydantic import BaseModel, Field
from typing import List, Dict, Any

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3)
    use_rag: bool = False
    strict: bool = False   # optional critic

class AgentMessage(BaseModel):
    agent: str
    content: str
    data: Dict[str, Any] = {}

class QueryResponse(BaseModel):
    run_id: str
    created_at: str
    user_query: str
    use_rag: bool
    strict: bool
    final_answer: str
    confidence: float
    sources: List[Dict[str, Any]]
    trace: List[AgentMessage]
