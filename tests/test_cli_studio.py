import pytest
import requests
import webbrowser
import subprocess
import sys
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

def test_studio_serve_with_backend_dir(monkeypatch):
    # Simule un backend dir via env
    monkeypatch.setenv('CREWAI_STUDIO_BACKEND_DIR', '/my/backend')
    calls = []
    monkeypatch.setattr(subprocess, 'run', lambda args, cwd, check: calls.append((args, cwd)))
    monkeypatch.setattr(sys, 'argv', ['squadmanager', 'studio', 'serve'])
    with pytest.raises(SystemExit) as exc:
        cli()
    assert exc.value.code == 0
    # Vérifie appel à streamlit via python -m
    expected = [sys.executable, '-m', 'streamlit', 'run', 'app.py', '--server.port', '8501']
    assert calls == [([sys.executable, '-m', 'streamlit', 'run', 'app.py', '--server.port', '8501'], '/my/backend')]

def test_studio_serve_default_dir(monkeypatch):
    # Pas de backend dir -> fallback
    monkeypatch.delenv('CREWAI_STUDIO_BACKEND_DIR', raising=False)
    calls = []
    monkeypatch.setattr(subprocess, 'run', lambda args, cwd, check: calls.append((args, cwd)))
    monkeypatch.setattr(sys, 'argv', ['squadmanager', 'studio', 'serve'])
    with pytest.raises(SystemExit) as exc:
        cli()
    assert exc.value.code == 0
    # Fallback devrait être 'D:/Scripts/CrewAI-Studio/app'
    assert calls[0][1].endswith('D:/Scripts/CrewAI-Studio/app')
    assert calls[0][0] == [sys.executable, '-m', 'streamlit', 'run', 'app.py', '--server.port', '8501']

def test_studio_stop_kills_process(monkeypatch, capsys):
    netstat_output = 'TCP    0.0.0.0:8501    0.0.0.0:0    LISTENING    12345\n'
    calls = []
    class FakeProc:
        def __init__(self, stdout):
            self.stdout = stdout
    def fake_run(args, capture_output=True, text=True, check=True, cwd=None):
        if args[0] == 'netstat':
            return FakeProc(netstat_output)
        calls.append(args)
        return FakeProc('')
    monkeypatch.setattr(subprocess, 'run', fake_run)
    monkeypatch.setattr(sys, 'argv', ['squadmanager', 'studio', 'stop'])
    with pytest.raises(SystemExit) as exc:
        cli()
    assert exc.value.code == 0
    assert calls == [['taskkill', '/PID', '12345', '/F']]
    assert capsys.readouterr().out.strip() == 'Streamlit arrêté.'

def test_studio_stop_no_process(monkeypatch, capsys):
    netstat_output = 'TCP    0.0.0.0:8502    0.0.0.0:0    LISTENING    12345\n'
    calls = []
    class FakeProc:
        def __init__(self, stdout):
            self.stdout = stdout
    def fake_run(args, capture_output=True, text=True, check=True, cwd=None):
        if args[0] == 'netstat':
            return FakeProc(netstat_output)
        calls.append(args)
        return FakeProc('')
    monkeypatch.setattr(subprocess, 'run', fake_run)
    monkeypatch.setattr(sys, 'argv', ['squadmanager', 'studio', 'stop'])
    with pytest.raises(SystemExit):
        cli()
    assert calls == []
    assert capsys.readouterr().out.strip() == 'Streamlit arrêté.'

def test_studio_restart_with_backend_dir(monkeypatch, capsys):
    # Simule un backend dir via env
    netstat_output = 'TCP    0.0.0.0:8501    0.0.0.0:0    LISTENING    34567\n'
    calls = []
    class FakeProc:
        def __init__(self, stdout):
            self.stdout = stdout
    def fake_run(args, capture_output=True, text=True, check=True, cwd=None):
        if args[0] == 'netstat':
            return FakeProc(netstat_output)
        calls.append((args, cwd))
        return FakeProc('')
    monkeypatch.setenv('CREWAI_STUDIO_BACKEND_DIR', '/my/backend')
    monkeypatch.setattr(subprocess, 'run', fake_run)
    monkeypatch.setattr(sys, 'argv', ['squadmanager', 'studio', 'restart'])
    with pytest.raises(SystemExit) as exc:
        cli()
    assert exc.value.code == 0
    # Vérifie d'abord l'arrêt puis le lancement
    assert calls[0] == (['taskkill', '/PID', '34567', '/F'], None)
    assert calls[1] == ([sys.executable, '-m', 'streamlit', 'run', 'app.py', '--server.port', '8501'], '/my/backend')

def test_studio_restart_default_dir(monkeypatch, capsys):
    # Pas de backend dir -> fallback
    netstat_output = 'TCP    0.0.0.0:8501    0.0.0.0:0    LISTENING    9876\n'
    calls = []
    class FakeProc:
        def __init__(self, stdout):
            self.stdout = stdout
    def fake_run(args, capture_output=True, text=True, check=True, cwd=None):
        if args[0] == 'netstat':
            return FakeProc(netstat_output)
        calls.append((args, cwd))
        return FakeProc('')
    monkeypatch.delenv('CREWAI_STUDIO_BACKEND_DIR', raising=False)
    monkeypatch.setattr(subprocess, 'run', fake_run)
    monkeypatch.setattr(sys, 'argv', ['squadmanager', 'studio', 'restart'])
    with pytest.raises(SystemExit) as exc:
        cli()
    assert exc.value.code == 0
    # Fallback doit utiliser le chemin par défaut
    assert calls[0] == (['taskkill', '/PID', '9876', '/F'], None)
    assert calls[1][0] == [sys.executable, '-m', 'streamlit', 'run', 'app.py', '--server.port', '8501']
    assert capsys.readouterr().out.strip() == 'Streamlit arrêté.'
