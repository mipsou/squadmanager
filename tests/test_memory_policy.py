import json
from datetime import datetime, timedelta
import pytest
from pathlib import Path

from dreamteam.memory import MemoryManager
from dreamteam.memory_policy import MemoryPolicy


def write_history(path, events):
    with open(path, 'w', encoding='utf-8') as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')


def test_ttl_policy(tmp_path):
    # Préparer history.jsonl avec anciens et récents
    now = datetime(2025, 5, 17, 12, 0, 0)
    old_ts = (now - timedelta(days=5)).isoformat()
    new_ts = now.isoformat()
    events = [
        {'val': 1, 'timestamp': old_ts},
        {'val': 2, 'timestamp': new_ts},
        {'val': 3}  # sans timestamp
    ]
    hist = tmp_path / 'history.jsonl'
    write_history(hist, events)
    mgr = MemoryManager(history_file=str(hist), db_file=str(tmp_path / 'db.sqlite'))
    policy = MemoryPolicy(ttl_days=1)
    kept = policy.apply(mgr, now=now)
    # Seuls les événements récents et sans timestamp sont conservés
    vals = [e.get('val') for e in kept]
    assert 1 not in vals
    assert 2 in vals
    assert 3 in vals
    # Le fichier a été réécrit
    reloaded = mgr.load_history()
    assert reloaded == kept


def test_lru_policy(tmp_path):
    # Préparer history.jsonl avec 10 événements datés
    now = datetime.now()
    events = []
    for i in range(10):
        # i=0 => 9min ago, i=9 => now
        ts = (now - timedelta(minutes=9-i)).isoformat()
        events.append({'i': i, 'timestamp': ts})
    hist = tmp_path / 'history.jsonl'
    write_history(hist, events)
    mgr = MemoryManager(history_file=str(hist), db_file=str(tmp_path / 'db.sqlite'))
    policy = MemoryPolicy(max_events=5)
    kept = policy.apply(mgr)
    # Conserver les 5 derniers événements (i=5..9)
    kept_i = [e.get('i') for e in kept]
    assert kept_i == [5, 6, 7, 8, 9]
    # Le fichier a été réécrit
    reloaded = mgr.load_history()
    assert reloaded == kept


def test_no_file(tmp_path):
    hist = tmp_path / 'history.jsonl'
    mgr = MemoryManager(history_file=str(hist), db_file=str(tmp_path / 'db.sqlite'))
    policy = MemoryPolicy(ttl_days=1, max_events=5)
    kept = policy.apply(mgr)
    assert kept == []
