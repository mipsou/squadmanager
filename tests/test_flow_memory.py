import pytest

from squadmanager.flow import squadmanagerFlow, squadmanagerState
import squadmanager.flow as flow_module
from squadmanager.crew import squadmanager

class FakeCrew:
    def __init__(self):
        self.inputs_called = []
    def kickoff(self, inputs):
        self.inputs_called.append(inputs)

class FakeMemMgr:
    def __init__(self):
        self.actions = []
    def load_history(self):
        self.actions.append('load_history')
    def append_event(self, event):
        self.actions.append(('append_event', event))
    def save_record(self, table, record):
        self.actions.append(('save_record', table, record))

@pytest.fixture(autouse=True)
def stub_dependencies(monkeypatch):
    """Stub MemoryManager et Crew pour tests flow_memory."""
    mem_mgr = FakeMemMgr()
    monkeypatch.setattr(flow_module, 'MemoryManager', lambda: mem_mgr)
    monkeypatch.setattr(squadmanager, 'crew', lambda self: FakeCrew())
    return mem_mgr

def test_run_flow_memory(monkeypatch):
    state = squadmanagerState(topic='T', year=2025)
    mem_mgr = flow_module.MemoryManager()
    crew_flow = squadmanagerFlow()

    result = crew_flow.run_flow(state)
    # Validate return state
    assert result == state
    # Validate memory orchestration actions
    assert mem_mgr.actions[0] == 'load_history'
    assert mem_mgr.actions[1][0] == 'append_event'
    assert mem_mgr.actions[1][1]['event'] == 'start_flow'
    # After crew kickoff
    assert mem_mgr.actions[2][0] == 'append_event'
    assert mem_mgr.actions[2][1]['event'] == 'end_flow'
    # Persistence record
    assert mem_mgr.actions[3][0] == 'save_record'
    assert mem_mgr.actions[3][1] == 'flow_runs'
    # Validate crew kickoff inputs
    crew_instance = crew_flow._last_crew
    assert crew_instance.inputs_called == [state.model_dump()]
