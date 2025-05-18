import os
import requests
from squadmanager.connectors import ExternalPlugin


class StudioPlugin(ExternalPlugin):
    """Plugin pour CrewAI Studio : health_check et envoi d'événements."""

    def __init__(self, config: dict):
        super().__init__(config)
        self.url = config.get('url') or os.getenv('CREWAI_STUDIO_URL', 'https://studio.crewai.com')
        self.token = config.get('api_key') or os.getenv('CREWAI_STUDIO_API_KEY')

    def health_check(self) -> dict:
        """Vérifie le status de l'API Studio."""
        headers = {}
        if self.token:
            headers['Authorization'] = f"Bearer {self.token}"
        resp = requests.get(f"{self.url}/api/status", headers=headers)
        return resp.json()

    def send_event(self, payload: dict) -> None:
        """Envoie un événement JSON à Studio."""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f"Bearer {self.token}"
        requests.post(f"{self.url}/api/events", json=payload, headers=headers)
