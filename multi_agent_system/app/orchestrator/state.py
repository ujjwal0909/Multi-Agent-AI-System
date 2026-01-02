from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import uuid

@dataclass
class RunState:
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_query: str = ""
    trace: List[Dict[str, Any]] = field(default_factory=list)
    artifacts: Dict[str, Any] = field(default_factory=dict)

    def add(self, agent: str, content: str, data: Optional[Dict[str, Any]] = None):
        self.trace.append({"agent": agent, "content": content, "data": data or {}})
