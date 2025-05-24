import json
import sys
import json
from pathlib import Path
import pytest

from squadmanager.cli import cli

def run_cli(args):
    sys.argv = ['squadmanager'] + args
    return cli()


def test_cli_demo_default(tmp_path, capsys):
    # Copie du template spec
    demo_template = Path(__file__).resolve().parents[1] / 'docs' / 'spec_template.md'
    # Exécution et capture de la sortie
    capsys.readouterr()
    run_cli(['demo'])
    # On s'attend à du JSON structuré
    captured = capsys.readouterr().out.strip()
    data = json.loads(captured)
    # Vérifier quelques clés du template
    assert 'Objectif' in data
    assert 'Fonctionnalités' in data
    assert 'Contraintes' in data


def test_cli_demo_custom(tmp_path, capsys):
    # Créer un template minimal
    content = '''
# A
B
'''
    tmpl = tmp_path / 'm.tmpl'
    tmpl.write_text(content, encoding='utf-8')
    # Exécution et capture de la sortie
    capsys.readouterr()
    run_cli(['demo', '--template', str(tmpl)])
    captured = capsys.readouterr().out.strip()
    data = json.loads(captured)
    assert 'A' in data and data['A'].strip() == 'B'

@pytest.mark.parametrize('invalid', [['demo', '--template']])
def test_cli_demo_missing_args(monkeypatch, invalid):
    # Should exit error if template manquant invalide
    monkeypatch.setenv('CREWAI_STORAGE_DIR', '')
    with pytest.raises(SystemExit):
        run_cli(invalid)
