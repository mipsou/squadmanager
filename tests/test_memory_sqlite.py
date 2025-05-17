import json
import sqlite3
from pathlib import Path
import pytest
from dreamteam.memory import MemoryManager


def test_init_db_creates_events_table(tmp_path):
    hist = tmp_path / 'history.jsonl'
    db = tmp_path / 'db.sqlite'
    mgr = MemoryManager(history_file=str(hist), db_file=str(db))
    # La table events doit exister
    conn = sqlite3.connect(str(mgr.db_path))
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events';")
    assert cursor.fetchone() is not None
    conn.close()


def test_append_event_inserts_jsonl_and_sqlite(tmp_path):
    hist = tmp_path / 'history.jsonl'
    db = tmp_path / 'db.sqlite'
    mgr = MemoryManager(history_file=str(hist), db_file=str(db))
    # Event avec timestamp explicite
    event = {'key': 'value', 'timestamp': '2025-05-17T19:00:00'}
    mgr.append_event(event)
    # Vérifier JSONL
    lines = hist.read_text(encoding='utf-8').splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == event
    # Vérifier SQLite
    conn = sqlite3.connect(str(mgr.db_path))
    rows = conn.execute("SELECT timestamp, payload FROM events;").fetchall()
    assert len(rows) == 1
    ts, payload = rows[0]
    assert ts == event['timestamp']
    assert json.loads(payload) == event
    conn.close()


def test_multiple_append_events_autoincrement_ids(tmp_path):
    hist = tmp_path / 'history.jsonl'
    db = tmp_path / 'db.sqlite'
    mgr = MemoryManager(history_file=str(hist), db_file=str(db))
    events = [ {'value': i, 'timestamp': f'2025-05-17T19:0{i}:00'} for i in range(3) ]
    for ev in events:
        mgr.append_event(ev)
    # Vérifier JSONL
    lines = hist.read_text(encoding='utf-8').splitlines()
    assert len(lines) == 3
    # Vérifier IDs autoincrémentés
    conn = sqlite3.connect(str(mgr.db_path))
    rows = conn.execute("SELECT id, timestamp FROM events ORDER BY id").fetchall()
    assert [r[0] for r in rows] == [1, 2, 3]
    assert [r[1] for r in rows] == [ev['timestamp'] for ev in events]
    conn.close()
