import json
import sqlite3

def log_event(event_type, data):
    """Ajoute un événement dans history.jsonl et org_memory.db"""
    evt = {"timestamp": data.get('timestamp'), "event_type": event_type, "data": data}
    # history.jsonl
    with open(os.path.join('src', 'dreamteam', 'memory', 'history.jsonl'), 'a') as f:
        f.write(json.dumps(evt) + '
')
    # org_memory.db
    conn = sqlite3.connect(os.path.join('src', 'dreamteam', 'memory', 'org_memory.db'))
    c = conn.cursor()
    c.execute("INSERT INTO events VALUES (?, ?, ?)", (evt['timestamp'], evt['event_type'], json.dumps(evt)))
    conn.commit()
    conn.close()
    print("Événement enregistré:", event_type)
