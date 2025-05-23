import pytest
import requests
from squadmanager.cli import auto_detect_studio_url

class FakeResp:
    def __init__(self, ok):
        self.ok = ok

    def json(self):
        return {'status': 'ok'}


def test_auto_detect_finds_8501(monkeypatch):
    calls = []
    def fake_get(url, timeout):
        calls.append(url)
        if 'localhost:8501' in url:
            return FakeResp(True)
        return FakeResp(False)
    monkeypatch.setattr(requests, 'get', fake_get)
    result = auto_detect_studio_url()
    assert result == 'http://localhost:8501'
    expected_ports = ['8000', '8080', '3000', '5000', '8501']
    called_ports = [url.split(':')[2].split('/')[0] for url in calls]
    assert called_ports == expected_ports


def test_auto_detect_no_service(monkeypatch):
    monkeypatch.setattr(requests, 'get', lambda url, timeout: FakeResp(False))
    assert auto_detect_studio_url() is None


def test_auto_detect_with_custom_ports(monkeypatch):
    calls = []
    def fake_get(url, timeout):
        calls.append(url)
        if 'localhost:1234' in url:
            return FakeResp(True)
        return FakeResp(False)
    monkeypatch.setattr(requests, 'get', fake_get)
    result = auto_detect_studio_url(ports=[1234, 5678])
    assert result == 'http://localhost:1234'
    assert calls and calls[0].startswith('http://localhost:1234')
