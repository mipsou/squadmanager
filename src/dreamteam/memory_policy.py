from datetime import datetime, timedelta
import json
import sqlite3

class MemoryPolicy:
    """
    Classe gérant les politiques d'éviction de la mémoire JSONL.
    Supporte TTL (jours) et LRU (nombre max d'événements).
    """
    def __init__(self, ttl_days: int = None, max_events: int = None,
                 eviction_policy: str = "lru"):
        self.ttl_days = ttl_days
        self.max_events = max_events
        self.eviction_policy = eviction_policy

    def apply(self, mgr, now: datetime = None) -> list:
        """
        Applique la politique au fichier history.jsonl de mgr.
        Retourne la liste des événements conservés.
        """
        path = mgr.history_path
        if not path.exists():
            return []
        events = mgr.load_history()
        # Filtrage TTL
        if self.ttl_days is not None:
            if now is None:
                now = datetime.now()
            cutoff = now - timedelta(days=self.ttl_days)
            filtered = []
            for e in events:
                ts = e.get("timestamp")
                if ts:
                    try:
                        dt = datetime.fromisoformat(ts)
                        if dt >= cutoff:
                            filtered.append(e)
                    except Exception:
                        filtered.append(e)
                else:
                    filtered.append(e)
            events = filtered
        # Filtrage LRU
        if self.max_events is not None and len(events) > self.max_events:
            # Conserve les derniers max_events événements
            events = events[-self.max_events:]
        # Réécriture du fichier
        with open(path, "w", encoding="utf-8") as f:
            for e in events:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        # Synchroniser avec SQLite: recréer la table events et insérer les événements conservés
        conn = sqlite3.connect(mgr.db_path)
        conn.execute("DROP TABLE IF EXISTS events")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                payload TEXT
            )
        """)
        for e in events:
            ts = e.get("timestamp") or datetime.now().isoformat()
            payload = json.dumps(e, ensure_ascii=False)
            conn.execute("INSERT INTO events (timestamp, payload) VALUES (?, ?)", (ts, payload))
        conn.commit()
        conn.close()
        return events
