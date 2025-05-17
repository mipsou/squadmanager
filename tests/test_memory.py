import pytest
from pathlib import Path
import sqlite3

from dreamteam.memory import MemoryManager


def test_append_and_load_history(tmp_path):
    history_file = tmp_path / "history.jsonl"
    db_file = tmp_path / "db.sqlite"
    mgr = MemoryManager(history_file=str(history_file), db_file=str(db_file))
    events = [{"a": 1}, {"b": "two"}]
    for e in events:
        mgr.append_event(e)
    loaded = mgr.load_history()
    assert loaded == events


def test_load_history_nonexistent(tmp_path):
    history_file = tmp_path / "history.jsonl"
    db_file = tmp_path / "db.sqlite"
    mgr = MemoryManager(history_file=str(history_file), db_file=str(db_file))
    loaded = mgr.load_history()
    assert loaded == []


def test_init_db_creates_file(tmp_path):
    history_file = tmp_path / "history.jsonl"
    db_file = tmp_path / "memory.db"
    mgr = MemoryManager(history_file=str(history_file), db_file=str(db_file))
    mgr.init_db()
    assert db_file.exists(), "Le fichier de base de données doit être créé"


def test_save_and_get_records(tmp_path):
    history_file = tmp_path / "history.jsonl"
    db_file = tmp_path / "memory.db"
    mgr = MemoryManager(history_file=str(history_file), db_file=str(db_file))
    mgr.init_db()
    record = {"id": 1, "value": "v"}
    mgr.save_record("test", record)
    recs = mgr.get_records("test")
    assert recs == [record]


def test_get_records_no_table(tmp_path):
    history_file = tmp_path / "history.jsonl"
    db_file = tmp_path / "memory.db"
    mgr = MemoryManager(history_file=str(history_file), db_file=str(db_file))
    mgr.init_db()
    recs = mgr.get_records("notable")
    assert recs == []
