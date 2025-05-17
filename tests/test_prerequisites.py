import shutil
import os
import pytest

def test_uv_available():
    """Vérifie que le CLI 'uv' est installé et accessible."""
    assert shutil.which("uv") is not None, \
        "Le CLI 'uv' doit être installé et accessible dans PATH"

def test_crewai_cli_available():
    """Vérifie que le CLI 'crewai' est installé et accessible."""
    assert shutil.which("crewai") is not None, \
        "Le CLI 'crewai' doit être installé et accessible dans PATH"

@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY non défini, test de prérequis ignoré")
def test_openai_api_key_set():
    """Vérifie que la variable d'environnement OPENAI_API_KEY est définie."""
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key and api_key.strip(), \
        "La variable d'environnement 'OPENAI_API_KEY' doit être définie"
