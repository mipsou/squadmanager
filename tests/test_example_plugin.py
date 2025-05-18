import sys
import pytest
import importlib.metadata
from squadmanager.plugin_manager import PluginManager
from squadmanager.plugins.example_plugin import ExamplePlugin

# Dummy entry point to simulate importlib.metadata entry_points
class DummyEP:
    def __init__(self, name, cls):
        self.name = name
        self._cls = cls
    def load(self):
        return self._cls


def test_example_plugin_loaded(monkeypatch):
    # Monkeypatch entry_points to return our example plugin EP
    def fake_entry_points(group=None):
        if group == 'squadmanager.plugins':
            return [DummyEP('example', ExamplePlugin)]
        return []
    monkeypatch.setattr(importlib.metadata, 'entry_points', fake_entry_points)

    mgr = PluginManager(config={'example': {'foo': 'bar'}})
    plugins = mgr.list_plugins()
    assert 'example' in plugins
    plugin = mgr.get_plugin('example')
    assert isinstance(plugin, ExamplePlugin)
    # health_check returns a dict
    assert plugin.health_check() == {'example': 'ok'}


def test_example_plugin_send_event(capsys, monkeypatch):
    plugin = ExamplePlugin(config={})
    plugin.send_event({'data': 123})
    captured = capsys.readouterr().out.strip()
    assert "ExamplePlugin: sent event {'data': 123}" in captured
