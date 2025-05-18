import sys
import pytest
import requests
import webbrowser
from squadmanager.cli import cli

class DummyResp:
    def __init__(self, data):
        self._data = data
    def json(self):
        return self._data


def test_studio_status(monkeypatch, capsys):
    monkeypatch.setenv('CREWAI_STUDIO_URL', 'http://test.studio')
    monkeypatch.setenv('CREWAI_STUDIO_API_KEY', 'token')
    # Mock requests.get
    monkeypatch.setattr(requests, 'get', lambda url, headers: DummyResp({'status': 'ok'}))
    # Simulate CLI args
    monkeypatch.setattr(sys, 'argv', ['squadmanager', 'studio', '--status'])
    with pytest.raises(SystemExit) as exc:
        cli()
    assert exc.value.code == 0
    out = capsys.readouterr().out.strip()
    assert out == '{"status": "ok"}' or out == '{"status":"ok"}'


def test_studio_open(monkeypatch):
    monkeypatch.setenv('CREWAI_STUDIO_URL', 'http://test.studio')
    calls = []
    # Mock webbrowser.open
    monkeypatch.setattr(webbrowser, 'open', lambda url: calls.append(url))
    monkeypatch.setattr(sys, 'argv', ['squadmanager', 'studio', '--open'])
    with pytest.raises(SystemExit) as exc:
        cli()
    assert exc.value.code == 0
    assert calls == ['http://test.studio']
