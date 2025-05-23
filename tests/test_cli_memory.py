import sys
import pytest
from io import StringIO
from contextlib import redirect_stdout
import subprocess

from squadmanager.cli import cli


def run_cli(args):
    sys.argv = ['squadmanager'] + args
    return cli()


def test_reset_memories_abort(monkeypatch, capsys):
    # Simulate input 'n'
    monkeypatch.setattr('builtins.input', lambda prompt: 'n')
    monkeypatch.setenv('CREWAI_STORAGE_DIR', '', prepend=False)
    with pytest.raises(SystemExit) as exc:
        run_cli(['reset-memories'])
    # Exit code 0 on abort
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert 'Abandon de la réinitialisation des mémoires' in captured.out


def test_reset_memories_confirm(monkeypatch):
    calls = []
    def fake_run(cmd, check):
        calls.append((cmd, check))
    monkeypatch.setattr(subprocess, 'run', fake_run)
    monkeypatch.setattr('builtins.input', lambda prompt: 'o')
    # Should not raise
    run_cli(['reset-memories'])
    assert calls == [(['crewai', 'reset-memories'], True)]


def test_reset_memories_force(monkeypatch):
    calls = []
    def fake_run(cmd, check):
        calls.append((cmd, check))
    monkeypatch.setattr(subprocess, 'run', fake_run)
    # With --force, no prompt
    run_cli(['reset-memories', '--force'])
    assert calls == [(['crewai', 'reset-memories'], True)]
