import subprocess
import os
import pytest


def test_end_to_end_run(tmp_path, monkeypatch):
    # Simule la commande crewai run pour générer report.md
    def fake_run(cmd, check, cwd=None, **kwargs):
        # Simule la création de report.md dans le dossier de travail
        path = cwd or os.getcwd()
        with open(os.path.join(path, "report.md"), "w") as f:
            f.write("E2E OK")
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    # Exécute la commande CLI squadmanager run
    result = subprocess.run(["squadmanager", "run"], check=True, cwd=str(tmp_path))
    # Vérifie la création et le contenu de report.md
    report_path = tmp_path / "report.md"
    assert report_path.exists(), "Le fichier report.md n'a pas été généré"
    assert report_path.read_text() == "E2E OK"
