import json
import sqlite3
import os
import appdirs
from pathlib import Path
from datetime import datetime
import json

class MemoryManager:
    """Gère l'historique JSONL et la base de données SQLite pour la mémoire."""
    def __init__(self, history_file: str = None, db_file: str = None):
        # Determine base storage directory via env or appdirs
        base_dir = Path(os.environ.get("CREWAI_STORAGE_DIR", appdirs.user_data_dir("dreamteam")))
        # Setup history file path
        if history_file:
            self.history_path = Path(history_file)
        else:
            self.history_path = base_dir / "history.jsonl"
        # Setup database file path
        if db_file:
            self.db_path = Path(db_file)
        else:
            self.db_path = base_dir / "org_memory.db"
        # Créer les répertoires si nécessaire
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # Initialiser la base et la table events
        self.init_db()

    def append_event(self, event: dict) -> None:
        """Ajoute un événement dans l'historique JSONL."""
        with open(self.history_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        # Enregistrez aussi dans SQLite
        conn = sqlite3.connect(self.db_path)
        ts = event.get("timestamp") or datetime.now().isoformat()
        payload = json.dumps(event, ensure_ascii=False)
        conn.execute(
            "INSERT INTO events (timestamp, payload) VALUES (?, ?)",
            (ts, payload)
        )
        conn.commit()
        conn.close()

    def load_history(self) -> list:
        """Lit et retourne la liste des événements depuis l'historique JSONL."""
        if not self.history_path.exists():
            return []
        events = []
        with open(self.history_path, "r", encoding="utf-8") as f:
            for line in f:
                events.append(json.loads(line))
        return events

    def init_db(self) -> None:
        """Initialise la base SQLite (crée le fichier si absent)."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                payload TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save_record(self, table: str, record: dict) -> None:
        """Insère un record dans la table SQLite (créée dynamiquement)."""
        conn = sqlite3.connect(self.db_path)
        cols = ", ".join(record.keys())
        placeholders = ", ".join("?" for _ in record)
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({cols})")
        conn.execute(
            f"INSERT INTO {table} ({cols}) VALUES ({placeholders})",
            tuple(record.values())
        )
        conn.commit()
        conn.close()

    def get_records(self, table: str) -> list:
        """Récupère tous les records d'une table SQLite sous forme de liste de dicts."""
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.execute(f"SELECT * FROM {table}")
        except sqlite3.OperationalError:
            conn.close()
            return []
        columns = [d[0] for d in cur.description]
        results = [dict(zip(columns, row)) for row in cur.fetchall()]
        conn.close()
        return results
