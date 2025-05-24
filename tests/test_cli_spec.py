import json
import sys
from io import StringIO
from contextlib import redirect_stdout
from pathlib import Path
import pytest
import builtins

from squadmanager.cli import cli

def run_cli(args):
    sys.argv = ['squadmanager'] + args
    return cli()


def test_cli_spec_parsing(tmp_path, capsys):
    content = '''
# Objectif
Permettre aux agents de test

# Fonctionnalités
- A
- B

# Contraintes
- C

# Livrables
Prototype

# Données requises
Données de test
'''  
    spec_file = tmp_path / 'spec.txt'
    spec_file.write_text(content, encoding='utf-8')
    run_cli(['spec', str(spec_file)])
    out = capsys.readouterr().out.strip()
    data = json.loads(out)
    # Vérification des clés et contenus
    assert 'Objectif' in data
    assert data['Objectif'].strip() == 'Permettre aux agents de test'
    assert 'Fonctionnalités' in data
    assert '- A' in data['Fonctionnalités']
    assert '- B' in data['Fonctionnalités']
    assert 'Contraintes' in data
    assert data['Contraintes'].strip() == '- C'
    assert 'Livrables' in data
    assert data['Livrables'].strip() == 'Prototype'
    assert 'Données requises' in data
    assert data['Données requises'].strip() == 'Données de test'


def test_cli_spec_interactive(monkeypatch, capsys):
    # Simuler mode interactif: on attend mode non implémenté, exit
    monkeypatch.setenv('CREWAI_STORAGE_DIR', '')
    monkeypatch.setattr(builtins, 'input', lambda: '')
    with pytest.raises(SystemExit):
        run_cli(['spec', '--interactive'])
