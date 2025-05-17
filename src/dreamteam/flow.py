from datetime import datetime
from datetime import datetime as dt
from pydantic import BaseModel
from dreamteam.crew import Dreamteam
from dreamteam.memory import MemoryManager

# Stub Flow et start decorator par défaut
class Flow:
    """Stub Flow si CrewAI Flows absent"""
    pass

def start(fn):
    """Stub decorator start"""
    return fn

# Optionnel: override stub si module Flow réel disponible
try:
    from crewai.flow.flow import Flow as _RealFlow, start as _RealStart
    Flow, start = _RealFlow, _RealStart
except Exception:
    pass


class DreamteamState(BaseModel):
    topic: str = "AI LLMs"
    year: int = dt.now().year


class DreamteamFlow(Flow):
    @start
    def run_flow(self, state: DreamteamState):
        """Kickoff Dreamteam crew via Flow avec orchestration de la mémoire."""
        # Orchestrer la mémoire externe (workflow étoile)
        mem_mgr = MemoryManager()
        # Charger l'historique
        mem_mgr.load_history()
        # Journaliser l'état avant exécution
        mem_mgr.append_event({"event": "start_flow", "state": state.dict()})
        # Exécuter la crew
        crew = Dreamteam().crew()
        # Archive crew instance pour tests
        self._last_crew = crew
        crew.kickoff(inputs=state.dict())
        # Journaliser l'état après exécution
        mem_mgr.append_event({"event": "end_flow", "state": state.dict()})
        # Persister une synthèse en base SQLite
        mem_mgr.save_record("flow_runs", {"topic": state.topic, "year": state.year})
        return state
