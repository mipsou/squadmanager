import os
import pytest
import requests
from squadmanager.plugins.studio_plugin import StudioPlugin

class DummyResponse:
    def __init__(self, json_data):
        self._json = json_data
    def json(self):
        return self._json

@ pytest.fixture(autouse=True)
def no_env(monkeypatch):
    # Ensure no env vars for studio
    monkeypatch.delenv('CREWAI_STUDIO_URL', raising=False)
    monkeypatch.delenv('CREWAI_STUDIO_API_KEY', raising=False)


def test_health_check_with_config(monkeypatch):
    dummy = DummyResponse({'status': 'ok'})
    called = {}
    def fake_get(url, headers=None):
        called['url'] = url
        called['headers'] = headers
        return dummy
    monkeypatch.setattr(requests, 'get', fake_get)
    plugin = StudioPlugin(config={'url': 'https://test', 'api_key': 'token123'})
    result = plugin.health_check()
    assert result == {'status': 'ok'}
    assert called['url'] == 'https://test/api/status'
    assert called['headers'] == {'Authorization': 'Bearer token123'}


def test_health_check_without_token(monkeypatch):
    dummy = DummyResponse({'health': 'ok'})
    monkeypatch.setenv('CREWAI_STUDIO_URL', 'https://envurl')
    monkeypatch.setenv('CREWAI_STUDIO_API_KEY', '')
    monkeypatch.setenv('CREWAI_STUDIO_API_KEY', '')
    called = {}
    monkeypatch.setattr(requests, 'get', lambda url, headers=None: DummyResponse({'health': 'ok'}))
    plugin = StudioPlugin(config={})
    result = plugin.health_check()
    assert result == {'health': 'ok'}


def test_send_event(monkeypatch):
    called = {}
    def fake_post(url, json, headers=None):
        called['url'] = url
        called['json'] = json
        called['headers'] = headers
        return None
    monkeypatch.setattr(requests, 'post', fake_post)
    plugin = StudioPlugin(config={'url': 'https://test2', 'api_key': 'keyXYZ'})
    payload = {'foo': 1}
    plugin.send_event(payload)
    assert called['url'] == 'https://test2/api/events'
    assert called['json'] == payload
    assert called['headers'] == {'Content-Type': 'application/json', 'Authorization': 'Bearer keyXYZ'}
