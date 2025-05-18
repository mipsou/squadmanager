import pytest
import socket
import subprocess
from pathlib import Path

HOST = "localhost"
PORT = 11434


def is_server_up(host, port, timeout=1):
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

@pytest.mark.skip(reason="KISS: CLI only wraps crewai run, does not write log file")
def test_real_cli_run(tmp_path):
    """
    Test d'intégration réel de la commande 'squadmanager run' contre un serveur Ollama.
    """
    # Forcer l’exécution réelle : échouer si le serveur Ollama n'est pas disponible
    assert is_server_up(HOST, PORT), f"Ollama server must be running at {HOST}:{PORT} for integration test"
    # Exécution réelle de la CLI
    result = subprocess.run(
        ["squadmanager", "run", "--topic", "IntegrationTest", "--current_year", "2025"],
        cwd=str(tmp_path),
        capture_output=True
    )
    assert result.returncode == 0, f"Exit code was {result.returncode}, stdout={result.stdout}, stderr={result.stderr}"
    log_path = Path(tmp_path) / "ollama.log"
    assert log_path.exists(), "Le fichier ollama.log n'a pas été créé"
    size = log_path.stat().st_size
    assert size > 0, "Le fichier de log est vide"
    content = log_path.read_text()
    assert "codellama:13b" in content, "Le log ne contient pas le chargement du modèle"
