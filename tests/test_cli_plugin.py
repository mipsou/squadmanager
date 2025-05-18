import sys
import json
import pytest
from contextlib import redirect_stdout
from io import StringIO

from squadmanager.cli import cli

class DummyPMList:
    def __init__(self, config=None): pass
    def list_plugins(self): return ["p1", "p2"]


def run_cli_and_capture(monkeypatch, args):
    monkeypatch.setattr(sys, 'argv', ['squadmanager'] + args)
    buf = StringIO()
    with redirect_stdout(buf):
        cli()
    return buf.getvalue().strip()


def test_cli_plugin_list(monkeypatch):
    import squadmanager.cli as cli_mod
    monkeypatch.setattr(cli_mod, 'PluginManager', DummyPMList)
    out = run_cli_and_capture(monkeypatch, ['plugin', 'list'])
    lines = out.splitlines()
    assert lines == ["p1", "p2"]

class DummyPlugin:
    def __init__(self, config=None): pass
    def health_check(self): return {"ok": True}
    def send_event(self, payload): setattr(self, 'payload', payload)

class DummyPMHealth:
    def __init__(self, config=None):
        self._plugins = {"test": DummyPlugin()}
    def list_plugins(self): return list(self._plugins.keys())
    def get_plugin(self, name): return self._plugins.get(name)


def test_cli_plugin_health(monkeypatch):
    import squadmanager.cli as cli_mod
    monkeypatch.setattr(cli_mod, 'PluginManager', DummyPMHealth)
    out = run_cli_and_capture(monkeypatch, ['plugin', 'health', '--plugin', 'test'])
    assert json.loads(out) == {"ok": True}


def test_cli_plugin_send(monkeypatch):
    import squadmanager.cli as cli_mod
    dp = DummyPlugin()
    class DummyPMSend(DummyPMHealth):
        def __init__(self, config=None):
            self._plugins = {"test": dp}
    monkeypatch.setattr(cli_mod, 'PluginManager', DummyPMSend)
    payload = {"a": 1}
    run_cli_and_capture(monkeypatch, ['plugin', 'send', '--plugin', 'test', '--payload', json.dumps(payload)])
    assert getattr(dp, 'payload') == payload
