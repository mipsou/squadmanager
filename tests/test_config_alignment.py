import pytest
from pathlib import Path
import yaml

def test_agents_in_tasks_are_defined():
    base_dir = Path(__file__).parent.parent / 'src' / 'squadmanager' / 'config'
    agents = yaml.safe_load(open(base_dir / 'agents.yaml', 'r', encoding='utf-8'))
    tasks = yaml.safe_load(open(base_dir / 'tasks.yaml', 'r', encoding='utf-8'))
    agent_keys = set(agents.keys())
    task_agents = {task['agent'] for task in tasks}
    missing = task_agents - agent_keys
    assert not missing, f"Agents in tasks.yaml not defined in agents.yaml: {missing}"
