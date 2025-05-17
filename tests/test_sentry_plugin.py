import os
import pytest
import sentry_sdk
from dreamteam.plugins.sentry_plugin import SentryPlugin

class DummyException(Exception):
    pass


def test_init_without_dsn_raises():
    with pytest.raises(ValueError) as excinfo:
        SentryPlugin(config={})
    assert 'DSN Sentry est manquant' in str(excinfo.value)


def test_init_with_dsn_from_config(monkeypatch):
    called = {}
    # stub sentry_sdk.init
    monkeypatch.setattr(sentry_sdk, 'init', lambda dsn=None, **kwargs: called.setdefault('dsn', dsn))
    plugin = SentryPlugin(config={'dsn': 'https://example.com/1'})
    assert plugin.health_check() == {'sentry': 'initialized'}
    assert called['dsn'] == 'https://example.com/1'


def test_init_with_env_dsn(monkeypatch):
    called = {}
    monkeypatch.setenv('CREWAI_SENTRY_DSN', 'https://example.com/2')
    monkeypatch.setattr(sentry_sdk, 'init', lambda dsn=None, **kwargs: called.setdefault('dsn', dsn))
    plugin = SentryPlugin(config={})
    assert called['dsn'] == 'https://example.com/2'


def test_send_event_message(monkeypatch, capsys):
    # stub init to avoid actual network
    monkeypatch.setattr(sentry_sdk, 'init', lambda **_: None)
    plugin = SentryPlugin(config={'dsn': 'dummy'})
    captured = {}
    monkeypatch.setattr(sentry_sdk, 'capture_message', lambda msg: captured.setdefault('message', msg))
    plugin.send_event({'key': 'value'})
    assert captured['message'] == str({'key': 'value'})


def test_send_event_exception(monkeypatch):
    monkeypatch.setattr(sentry_sdk, 'init', lambda **_: None)
    plugin = SentryPlugin(config={'dsn': 'dummy'})
    captured_exc = {}
    monkeypatch.setattr(sentry_sdk, 'capture_exception', lambda e: captured_exc.setdefault('exception', e))
    exc = DummyException('oops')
    plugin.send_event({'exception': exc})
    assert captured_exc['exception'] is exc
