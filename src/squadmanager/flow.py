from datetime import datetime as dt
from pydantic import BaseModel
from squadmanager.crew import squadmanager
from squadmanager.memory import MemoryManager

# Stub Flow et start decorator par défaut
class Flow:
    """Stub Flow si CrewAI Flows absent"""
    pass

def start(fn):
    """Stub decorator start"""
    return fn

class DreamteamState(BaseModel):
    topic: str = "AI LLMs"
    year: int = dt.now().year


class DreamteamFlow(Flow):
    @start
    def run_flow(self, state: DreamteamState):
        """Kickoff squadmanager crew via Flow avec orchestration de la mémoire."""
        # Orchestrer la mémoire externe (workflow étoile)
        mem_mgr = MemoryManager()
        # Charger l'historique
        mem_mgr.load_history()
        # Journaliser l'état avant exécution
        mem_mgr.append_event({"event": "start_flow", "state": state.model_dump()})
        # Exécuter la crew
        crew = squadmanager().crew()
        # Archive crew instance pour tests
        self._last_crew = crew
        crew.kickoff(inputs=state.model_dump())
        # Journaliser l'état après exécution
        mem_mgr.append_event({"event": "end_flow", "state": state.model_dump()})
        # Persister une synthèse en base SQLite
        mem_mgr.save_record("flow_runs", {"topic": state.topic, "year": state.year})
        return state
