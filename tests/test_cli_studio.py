import sys
import pytest
import requests
import webbrowser
from squadmanager.cli import cli
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock

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

@patch('squadmanager.cli.requests.get')
@patch('squadmanager.cli.os.getenv', return_value=None)
def test_studio_list(mock_getenv, mock_get, capsys, tmp_path):
    # Mock response JSON
    mock_resp = MagicMock()
    mock_resp.json.return_value = [{'id': '1', 'name': 'Crew1'}]
    mock_get.return_value = mock_resp

    # Simulate CLI args
    sys.argv = ['squadmanager', 'studio', 'list']
    import squadmanager.cli as cli_module
    cli_module.cli()

    captured = capsys.readouterr()
    data = yaml.safe_load(captured.out)
    assert data == [{'id': '1', 'name': 'Crew1'}]

@patch('squadmanager.cli.requests.get')
@patch('squadmanager.cli.os.getenv', return_value=None)
def test_studio_export_stdout(mock_getenv, mock_get, capsys, tmp_path):
    mock_resp = MagicMock()
    crew_data = {'id': '2', 'config': {'foo': 'bar'}}
    mock_resp.json.return_value = crew_data
    mock_get.return_value = mock_resp

    sys.argv = ['squadmanager', 'studio', 'export', '2']
    import squadmanager.cli as cli_module
    cli_module.cli()

    captured = capsys.readouterr()
    data = yaml.safe_load(captured.out)
    assert data == crew_data

@patch('squadmanager.cli.requests.get')
@patch('squadmanager.cli.os.getenv', return_value=None)
def test_studio_export_file(mock_getenv, mock_get, tmp_path):
    mock_resp = MagicMock()
    crew_data = {'id': '3', 'config': {'x': 1}}
    mock_resp.json.return_value = crew_data
    mock_get.return_value = mock_resp
    out_file = tmp_path / 'out.yaml'

    sys.argv = ['squadmanager', 'studio', 'export', '3', '-o', str(out_file)]
    import squadmanager.cli as cli2
    cli2.cli()

    content = yaml.safe_load(out_file.read_text(encoding='utf-8'))
    assert content == crew_data

@patch('squadmanager.cli.requests.post')
@patch('squadmanager.cli.os.getenv', return_value=None)
def test_studio_import(mock_getenv, mock_post, capsys, tmp_path):
    crew_yaml = {'id': '4', 'cfg': {'a': 2}}
    file = tmp_path / 'in.yaml'
    file.write_text(yaml.safe_dump(crew_yaml), encoding='utf-8')

    mock_resp = MagicMock()
    mock_resp.json.return_value = {'status': 'ok'}
    mock_post.return_value = mock_resp

    sys.argv = ['squadmanager', 'studio', 'import', str(file)]
    import squadmanager.cli as cli_module
    cli_module.cli()

    captured = capsys.readouterr()
    result = yaml.safe_load(captured.out)
    assert result == {'status': 'ok'}
