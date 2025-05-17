import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import pytest

from dreamteam.cli import cli


def run_cli(args):
    sys.argv = ['dreamteam'] + args
    return cli()


def write_history(path: Path, events: list):
    with open(path, 'w', encoding='utf-8') as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')


def test_cli_apply_ttl(tmp_path, monkeypatch, capsys):
    # Prepare history with old and new events
    now = datetime(2025, 5, 17, 12, 0, 0)
    old_ts = (now - timedelta(days=5)).isoformat()
    new_ts = now.isoformat()
    events = [
        {'val': 1, 'timestamp': old_ts},
        {'val': 2, 'timestamp': new_ts},
        {'val': 3}
    ]
    # Set storage dir
    monkeypatch.setenv('CREWAI_STORAGE_DIR', str(tmp_path))
    hist = tmp_path / 'history.jsonl'
    write_history(hist, events)
    # Apply TTL = 1 day
    out = run_cli(['memory-apply-policy', '--ttl-days', '1'])
    captured = capsys.readouterr().out
    assert 'Événements conservés suite à la politique: 2' in captured
    # File rewritten
    with open(hist, 'r', encoding='utf-8') as f:
        kept = [json.loads(line) for line in f]
    vals = sorted(e['val'] for e in kept)
    assert vals == [2, 3]


def test_cli_apply_max_events(tmp_path, monkeypatch, capsys):
    # Prepare history with 5 events
    now = datetime.now()
    events = []
    for i in range(5):
        ts = (now - timedelta(minutes=5-i)).isoformat()
        events.append({'i': i, 'timestamp': ts})
    monkeypatch.setenv('CREWAI_STORAGE_DIR', str(tmp_path))
    hist = tmp_path / 'history.jsonl'
    write_history(hist, events)
    # Apply max-events = 3
    run_cli(['memory-apply-policy', '--max-events', '3'])
    captured = capsys.readouterr().out
    assert 'Événements conservés suite à la politique: 3' in captured
    # File rewritten
    with open(hist, 'r', encoding='utf-8') as f:
        kept = [json.loads(line) for line in f]
    kept_i = [e['i'] for e in kept]
    assert kept_i == [2, 3, 4]


def test_cli_apply_both(tmp_path, monkeypatch, capsys):
    # Prepare history with 5 events, old timestamp for first
    now = datetime(2025, 5, 17, 12, 0, 0)
    events = []
    # First old
    events.append({'i': 0, 'timestamp': (now - timedelta(days=5)).isoformat()})
    # Next 4 recent
    for i in range(1, 5):
        ts = now.isoformat()
        events.append({'i': i, 'timestamp': ts})
    monkeypatch.setenv('CREWAI_STORAGE_DIR', str(tmp_path))
    hist = tmp_path / 'history.jsonl'
    write_history(hist, events)
    # Apply TTL=2, max-events=2 => keep only two most recent after TTL filter
    run_cli(['memory-apply-policy', '--ttl-days', '2', '--max-events', '2'])
    captured = capsys.readouterr().out
    assert 'Événements conservés suite à la politique: 2' in captured
    # File rewritten
    with open(hist, 'r', encoding='utf-8') as f:
        kept = [json.loads(line) for line in f]
    kept_i = [e['i'] for e in kept]
    assert kept_i == [3, 4]
