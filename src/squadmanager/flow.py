from datetime import datetime
from datetime import datetime as dt
from dataclasses import dataclass, asdict
from squadmanager.crew import squadmanager
import os
from mcp import StdioServerParameters
from crewai_tools import MCPServerAdapter
from squadmanager.memory import MemoryManager
import yaml
from pathlib import Path

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


@dataclass
class squadmanagerState:
    topic: str = "AI LLMs"
    year: int = dt.now().year

    def model_dump(self):
        return asdict(self)


class squadmanagerFlow(Flow):
    @start
    def run_flow(self, state: squadmanagerState):
        """Kickoff squadmanager crew via Flow avec orchestration de la mémoire."""
        # Orchestrer la mémoire externe (workflow étoile)
        mem_mgr = MemoryManager()
        # Charger inputs depuis YAML
        config_dir = Path(__file__).parent
        pdg_file = config_dir / "pdg_input.yaml"
        client_file = config_dir / "client_input.yaml"
        pdg_inputs = yaml.safe_load(pdg_file.read_text()) if pdg_file.exists() else {}
        client_inputs = yaml.safe_load(client_file.read_text()) if client_file.exists() else {}
        inputs = {**state.model_dump(), **pdg_inputs, **client_inputs}
        # Charger l'historique
        mem_mgr.load_history()
        # Journaliser l'état avant exécution
        mem_mgr.append_event({"event": "start_flow", "state": state.model_dump()})
        # Exécuter la crew
        crew = squadmanager().crew()
        # Inject MCP tools dans chaque agent (KISS)
        params = StdioServerParameters(
            command=os.getenv("MCP_COMMAND", "uvx"),
            args=os.getenv("MCP_ARGS", "").split(),
            env=dict(os.environ),
        )
        mcp_adapter = MCPServerAdapter(params)
        for ag in crew.agents:
            setattr(ag, 'tools', getattr(ag, 'tools', []) + [mcp_adapter])
        # Archive crew instance pour tests
        self._last_crew = crew
        crew.kickoff(inputs=inputs)
        # Journaliser l'état après exécution
        mem_mgr.append_event({"event": "end_flow", "state": state.model_dump()})
        # Persister une synthèse en base SQLite
        mem_mgr.save_record("flow_runs", {"topic": state.topic, "year": state.year})
        return state
