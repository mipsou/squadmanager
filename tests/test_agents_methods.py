import yaml
import pytest
from pathlib import Path
from dreamteam.crew import Dreamteam

def test_agent_methods_exist():
    # Charger la configuration des agents
    base_dir = Path(__file__).parent.parent / "src" / "dreamteam" / "config"
    agents_cfg = yaml.safe_load((base_dir / "agents.yaml").read_text())
    dream = Dreamteam()
    for agent_name in agents_cfg.keys():
        assert hasattr(dream, agent_name), f"Dreamteam missing method '{agent_name}'"
        method = getattr(dream, agent_name)
        assert callable(method), f"Attribute '{agent_name}' is not callable"
