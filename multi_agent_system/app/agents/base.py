from abc import ABC, abstractmethod
from app.orchestrator.state import RunState

class Agent(ABC):
    name: str

    @abstractmethod
    def run(self, state: RunState) -> None:
        ...
