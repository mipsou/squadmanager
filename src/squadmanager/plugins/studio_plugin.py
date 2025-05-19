import os
import requests
from squadmanager.connectors import ExternalPlugin


class StudioPlugin(ExternalPlugin):
    """Plugin pour interagir avec CrewAI Studio (health & events)"""

    def __init__(self, config: dict):
        super().__init__(config)
        # URL de base du service
        self.url = config.get('url') or os.getenv('CREWAI_STUDIO_URL')
        if not self.url:
            raise ValueError('URL Studio est manquant')
        # Clé API facultative
        self.api_key = config.get('api_key') or os.getenv('CREWAI_STUDIO_API_KEY')

    def health_check(self) -> dict:
        status_url = f"{self.url.rstrip('/')}" + "/api/status"
        headers = {}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.get(status_url, headers=headers)
        return response.json()

    def send_event(self, payload: dict) -> None:
        events_url = f"{self.url.rstrip('/')}" + "/api/events"
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        requests.post(events_url, json=payload, headers=headers)
