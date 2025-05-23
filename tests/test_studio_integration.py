import pytest
import subprocess
import requests
import time
import os
import sys
import yaml
from pathlib import Path
from squadmanager.plugins.studio_plugin import StudioPlugin

# Hôte du backend REST
BACKEND_HOST = 'http://localhost:8000'

@ pytest.fixture(scope='session')
def studio_backend():
    """Démarre le backend REST en uvicorn et attend qu'il soit disponible"""
    try:
        import crewai_studio.main  # vérifier que le package est installé
    except ImportError:
        pytest.skip("Package crewai_studio non installé, tests d'intégration ignorés")
    # Lancer uvicorn via python -m
    cmd = [sys.executable, '-m', 'uvicorn', 'crewai_studio.main:app', '--reload', '--port', '8000']
    proc = subprocess.Popen(cmd)
    # Attente du démarrage
    url = f"{BACKEND_HOST}/api/status"
    for _ in range(10):
        try:
            r = requests.get(url, timeout=1)
            if r.ok:
                break
        except requests.RequestException:
            time.sleep(1)
    else:
        proc.terminate()
        pytest.skip('Le backend REST n\u2019a pas démarré')

    yield BACKEND_HOST

    proc.terminate()
    proc.wait()


def test_import_and_list_integration(studio_backend):
    """Test d'intégration complet : import et listing du crew via HTTP"""
    plugin = StudioPlugin(config={'url': studio_backend})
    # Charger la config YAML
    yml_path = Path(__file__).resolve().parents[1] / 'squadmanagerAI.yml'
    crew_cfg = yaml.safe_load(yml_path.read_text(encoding='utf-8'))
    # Import
    res = plugin.import_crew(crew_cfg)
    assert 'id' in res
    # List
    list_res = plugin.list_crews()
    assert any(c.get('name') == crew_cfg.get('name') for c in list_res)
