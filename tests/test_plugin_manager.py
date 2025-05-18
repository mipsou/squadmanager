import pytest
from squadmanager.plugin_manager import PluginManager

def test_no_plugins(monkeypatch):
    # Simule un entry_points vide
    monkeypatch.setattr('importlib.metadata.entry_points', lambda group=None: [] if group=='squadmanager.plugins' else {})
    mgr = PluginManager()
    assert mgr.list_plugins() == []
