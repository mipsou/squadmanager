# Préparer modules factices pour crewai.memory
import sys, types
sys.modules.setdefault('crewai', types.ModuleType('crewai'))
sys.modules['crewai.memory'] = types.ModuleType('crewai.memory')
sys.modules['crewai.memory.storage'] = types.ModuleType('crewai.memory.storage')
sys.modules['crewai.memory.storage.rag_storage'] = types.ModuleType('crewai.memory.storage.rag_storage')
sys.modules['crewai.memory.storage.ltm_sqlite_storage'] = types.ModuleType('crewai.memory.storage.ltm_sqlite_storage')

# Puis imports existants
import pytest
import yaml
from pathlib import Path

import squadmanager.crew as crew_module
from squadmanager.crew import squadmanager

import crewai.memory as memory_module
import crewai.memory.storage.rag_storage as rag_storage_module
import crewai.memory.storage.ltm_sqlite_storage as ltm_module

class DummyShortTermMemory:
    def __init__(self, storage):
        self.storage = storage

class DummyLongTermMemory:
    def __init__(self, storage):
        self.storage = storage

class DummyEntityMemory:
    def __init__(self, storage):
        self.storage = storage

class DummyRAGStorage:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

class DummyLTMSQLiteStorage:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

class FakeCrew:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

@pytest.fixture(autouse=True)
def stub_memory_injection(monkeypatch):
    # Stub squadmanager crew création
    monkeypatch.setattr(crew_module, 'Crew', FakeCrew)
    # Stub memory classes
    monkeypatch.setattr(memory_module, 'ShortTermMemory', DummyShortTermMemory, raising=False)
    monkeypatch.setattr(memory_module, 'LongTermMemory', DummyLongTermMemory, raising=False)
    monkeypatch.setattr(memory_module, 'EntityMemory', DummyEntityMemory, raising=False)
    monkeypatch.setattr(rag_storage_module, 'RAGStorage', DummyRAGStorage, raising=False)
    monkeypatch.setattr(ltm_module, 'LTMSQLiteStorage', DummyLTMSQLiteStorage, raising=False)


def test_memory_config_injection(tmp_path):
    # Prepare config directory and memory.yaml
    config_dir = tmp_path / 'config'
    config_dir.mkdir()
    # Créer fichiers agents.yaml et tasks.yaml vides pour test
    (config_dir / 'agents.yaml').write_text(yaml.dump({}))
    (config_dir / 'tasks.yaml').write_text(yaml.dump([]))
    mem_conf = {
        'short_term_memory': {
            'storage': {
                'embedder_config': {'provider': 'openai', 'config': {'model': 'test-model'}},
                'type': 'short_term',
                'path': '/tmp'
            }
        },
        'long_term_memory': {
            'storage': {'db_path': 'test.db'}
        },
        'entity_memory': {
            'storage': {
                'embedder_config': {'provider': 'openai', 'config': {'model': 'test-model'}},
                'type': 'entity',
                'path': '/tmp'
            }
        }
    }
    (config_dir / 'memory.yaml').write_text(yaml.dump(mem_conf))
    # Instantiate with config_path
    dt = squadmanager(config_path=str(config_dir))
    crew_inst = dt.crew()
    kwargs = crew_inst.kwargs
    # Validate native memory flag
    assert kwargs.get('memory', False) is True
    # Validate short-term memory injection
    assert 'short_term_memory' in kwargs
    st = kwargs['short_term_memory']
    assert isinstance(st, DummyShortTermMemory)
    assert isinstance(st.storage, DummyRAGStorage)
    assert st.storage.kwargs['type'] == 'short_term'
    # Validate long-term memory injection
    assert 'long_term_memory' in kwargs
    lt = kwargs['long_term_memory']
    assert isinstance(lt, DummyLongTermMemory)
    assert isinstance(lt.storage, DummyLTMSQLiteStorage)
    assert lt.storage.kwargs['db_path'] == 'test.db'
    # Validate entity memory injection
    assert 'entity_memory' in kwargs
    em = kwargs['entity_memory']
    assert isinstance(em, DummyEntityMemory)
    assert isinstance(em.storage, DummyRAGStorage)
    assert em.storage.kwargs['type'] == 'entity'
