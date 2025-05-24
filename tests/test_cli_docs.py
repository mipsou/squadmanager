import sys
from pathlib import Path

import pytest
import squadmanager.cli as cli_module


def test_run_with_docs(monkeypatch, tmp_path):
    # Create dummy docs in tmp_path
    d1 = tmp_path / "b.txt"
    d1.write_text("doc1")
    d2 = tmp_path / "a.txt"
    d2.write_text("doc2")

    # Prepare argv with docs in reverse order
    monkeypatch.setattr(sys, "argv", ["squadmanager", "run", "--docs", str(d1), str(d2)])

    # Capture subprocess.run calls
    calls = []
    def fake_run(cmd, check):
        calls.append(cmd)
    monkeypatch.setattr(cli_module.subprocess, "run", fake_run)

    # Execute CLI
    cli_module.cli()

    # Expected sorted absolute docs paths
    expected_paths = sorted([d1.resolve().as_posix(), d2.resolve().as_posix()])
    assert calls, "subprocess.run should be called"
    assert calls[0] == ["crewai", "run", "--docs"] + expected_paths
