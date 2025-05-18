import os
from pathlib import Path
import appdirs
import pytest

from squadmanager.memory import MemoryManager


def test_default_paths_without_env(monkeypatch, tmp_path):
    # Simuler absence de variable d'environnement
    monkeypatch.delenv("CREWAI_STORAGE_DIR", raising=False)
    # Rediriger user_data_dir vers tmp_path
    monkeypatch.setattr(appdirs, 'user_data_dir', lambda appname: str(tmp_path))
    mgr = MemoryManager()
    assert mgr.history_path == tmp_path / "history.jsonl"
    assert mgr.db_path == tmp_path / "org_memory.db"


def test_paths_with_env(monkeypatch, tmp_path):
    # Définir la variable d'environnement
    custom = tmp_path / "custom_dir"
    monkeypatch.setenv("CREWAI_STORAGE_DIR", str(custom))
    mgr = MemoryManager()
    assert mgr.history_path == custom / "history.jsonl"
    assert mgr.db_path == custom / "org_memory.db"
