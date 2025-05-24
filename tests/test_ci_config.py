import pytest
from pathlib import Path


def test_ci_workflow_file_exists():
    path = Path(__file__).resolve().parents[1] / '.github' / 'workflows' / 'ci.yml'
    assert path.exists(), '.github/workflows/ci.yml manquant'


def test_ci_yaml_has_pytest_and_flake8():
    path = Path(__file__).resolve().parents[1] / '.github' / 'workflows' / 'ci.yml'
    content = path.read_text(encoding='utf-8')
    assert 'pytest' in content, 'pytest non configuré dans ci.yml'
    assert 'flake8' in content, 'flake8 non configuré dans ci.yml'
