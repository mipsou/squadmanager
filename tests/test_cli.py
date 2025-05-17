import sys
import pytest
from contextlib import redirect_stdout
from io import StringIO
import subprocess

from dreamteam.cli import cli
from dreamteam.core import DreamTeam
from dreamteam.flow import DreamteamFlow, DreamteamState


def run_cli(monkeypatch, args):
    monkeypatch.setattr(sys, 'argv', ['dreamteam'] + args)
    return cli()


def run_cli_and_capture(monkeypatch, args):
    monkeypatch.setattr(sys, 'argv', ['dreamteam'] + args)
    buf = StringIO()
    with redirect_stdout(buf):
        cli()
    return buf.getvalue().strip()


def test_help(monkeypatch, capsys):
    with pytest.raises(SystemExit):
        run_cli(monkeypatch, ['--help'])
    out = capsys.readouterr().out
    assert 'usage: dreamteam' in out


def test_unknown_command(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['dreamteam', 'invalid_cmd'])
    with pytest.raises(SystemExit):
        cli()
    err = capsys.readouterr().err
    assert 'invalid choice' in err


def test_cli_create_project(monkeypatch):
    out = run_cli_and_capture(monkeypatch, ['create_project', 'proj'])
    assert out == 'Project proj created'


def test_cli_create_team(monkeypatch):
    out = run_cli_and_capture(monkeypatch, ['create_team', 'team1'])
    assert out == 'Team team1 created'


def test_cli_define_kpi(monkeypatch):
    out = run_cli_and_capture(monkeypatch, ['define_kpi', 'a', 'desc'])
    assert 'KPI a defined' in out


def test_cli_increment_kpi(monkeypatch):
    monkeypatch.setattr(DreamTeam, 'increment_kpi', lambda self, name, amount: None)
    monkeypatch.setattr(DreamTeam, 'get_kpi', lambda self, name: 7)
    out = run_cli_and_capture(monkeypatch, ['increment_kpi', 'a', '--amount', '2'])
    assert out == '7'


def test_cli_get_kpi(monkeypatch):
    monkeypatch.setattr(DreamTeam, 'get_kpi', lambda self, name: 5)
    out = run_cli_and_capture(monkeypatch, ['get_kpi', 'a'])
    assert out == '5'


def test_cli_list_kpis(monkeypatch):
    monkeypatch.setattr(DreamTeam, 'get_all_kpis', lambda self: {'a': {'value': 3, 'description': 'desc'}})
    out = run_cli_and_capture(monkeypatch, ['list_kpis'])
    assert 'a: 3 -- desc' in out


def test_cli_crewai_test(monkeypatch):
    calls = []
    def fake_run(cmd, check=True):
        calls.append((tuple(cmd), check))
    monkeypatch.setattr(subprocess, 'run', fake_run)
    # Execute the crewai_test command
    run_cli_and_capture(monkeypatch, ['crewai_test'])
    assert calls == [
        (('pytest', '-v', '--maxfail=1', '-s'), True),
        (('crewai', 'test'), True)
    ]


def test_cli_flow(monkeypatch):
    calls = []
    def fake_run_flow(self, state):
        calls.append(state)
        return state
    monkeypatch.setattr(DreamteamFlow, 'run_flow', fake_run_flow)
    out = run_cli_and_capture(monkeypatch, ['flow', '--topic', 'TestTopic', '--year', '2025'])
    assert out == ''
    assert len(calls) == 1, "Le flow doit être exécuté une fois"
    state = calls[0]
    assert state.topic == 'TestTopic'
    assert state.year == 2025
