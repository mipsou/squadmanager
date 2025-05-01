import subprocess
import os
import pytest
import sys
import pathlib


def test_cli_run_end_to_end(tmp_path, monkeypatch):
    """
    End-to-end test of CLI 'dreamteam run' ensuring crewai run is invoked and logs are produced.
    """
    # Stub subprocess.run for 'crewai run'
    def fake_run(cmd, check, stdout=None, stderr=None, cwd=None, **kwargs):
        # Vérifier que c'est bien crewai run
        assert cmd == ["crewai", "run"]
        # Simuler écriture du log Ollama
        log_path = pathlib.Path(cwd or os.getcwd()) / "ollama.log"
        log_path.write_text("Chargement du modèle codellama:13b")
        return subprocess.CompletedProcess(cmd, 0)

    # Monkeypatch subprocess.run globally
    monkeypatch.setattr(subprocess, "run", fake_run)

    # Exécuter la CLI dans tmp_path avec l’argument 'run'
    orig_cwd = os.getcwd()
    os.chdir(tmp_path)
    monkeypatch.setattr(sys, 'argv', ['dreamteam', 'run'])
    try:
        from dreamteam.cli import cli
        cli()
    finally:
        os.chdir(orig_cwd)

    # Vérifier la création et le contenu du fichier de log
    log_file = tmp_path / "ollama.log"
    assert log_file.exists(), "Le fichier ollama.log n'a pas été créé"
    content = log_file.read_text()
    assert "codellama:13b" in content, "Le log ne contient pas le chargement du modèle"
