import os
import requests
from squadmanager.connectors import ExternalPlugin
from squadmanager.utils import auto_detect_studio_url


class StudioPlugin(ExternalPlugin):
    """Plugin pour interagir avec CrewAI Studio (health & events)"""

    def __init__(self, config: dict):
        super().__init__(config)
        # URL de base du service (priorité: config > env > détection auto > public)
        env_url = os.getenv('CREWAI_STUDIO_URL')
        url = config.get('url') or env_url or auto_detect_studio_url() or 'https://studio.crewai.com'
        self.url = url.rstrip('/')
        # Clé API facultative
        self.api_key = config.get('api_key') or os.getenv('CREWAI_STUDIO_API_KEY')

    def health_check(self) -> dict:
        status_url = f"{self.url}" + "/api/status"
        headers = {}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.get(status_url, headers=headers)
        return response.json()

    def send_event(self, payload: dict) -> None:
        events_url = f"{self.url}" + "/api/events"
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        requests.post(events_url, json=payload, headers=headers)

    def open_ui(self) -> None:
        """Ouvre l’UI de CrewAI Studio dans le navigateur."""
        import webbrowser, os
        from urllib.parse import urlparse, urlunparse
        # Priorité à l'URL UI explicite
        ui_url = os.getenv('CREWAI_STUDIO_UI_URL')
        if not ui_url:
            parsed = urlparse(self.url)
            # Si localhost, ouvrir UI Streamlit sur port 8501
            if parsed.hostname in ('localhost', '127.0.0.1'):
                netloc = f"{parsed.hostname}:8501"
                ui_url = urlunparse(parsed._replace(netloc=netloc))
            else:
                # Instance publique ou distante : ouvrir tel quelle
                ui_url = self.url
        webbrowser.open(ui_url)

    def list_crews(self) -> list:
        """Liste les crews existants dans CrewAI Studio."""
        url = f"{self.url}/api/crews"
        headers = {}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.get(url, headers=headers)
        return response.json()

    def export_crew(self, crew_id: str) -> dict:
        """Exporte la configuration d'un crew depuis CrewAI Studio."""
        url = f"{self.url}/api/crews/{crew_id}"
        headers = {'Accept': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.get(url, headers=headers)
        return response.json()

    def import_crew(self, crew_config: dict) -> dict:
        """Importe un crew dans CrewAI Studio depuis un dict."""
        url = f"{self.url}/api/crews"
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.post(url, json=crew_config, headers=headers)
        return response.json()

    def list_agents(self) -> list:
        """Liste les agents existants dans CrewAI Studio."""
        url = f"{self.url}/api/agents"
        headers = {}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.get(url, headers=headers)
        return response.json()

    def export_agent(self, agent_id: str) -> dict:
        """Exporte la configuration d'un agent depuis CrewAI Studio."""
        url = f"{self.url}/api/agents/{agent_id}"
        headers = {'Accept': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.get(url, headers=headers)
        return response.json()

    def import_agent(self, agent_config: dict) -> dict:
        """Importe un agent dans CrewAI Studio depuis un dict."""
        url = f"{self.url}/api/agents"
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.post(url, json=agent_config, headers=headers)
        return response.json()

    def list_tasks(self) -> list:
        """Liste les tâches existantes dans CrewAI Studio."""
        url = f"{self.url}/api/tasks"
        headers = {}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.get(url, headers=headers)
        return response.json()

    def export_task(self, task_id: str) -> dict:
        """Exporte la configuration d'une tâche depuis CrewAI Studio."""
        url = f"{self.url}/api/tasks/{task_id}"
        headers = {'Accept': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.get(url, headers=headers)
        return response.json()

    def import_task(self, task_config: dict) -> dict:
        """Importe une tâche dans CrewAI Studio depuis un dict."""
        url = f"{self.url}/api/tasks"
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.post(url, json=task_config, headers=headers)
        return response.json()

    def delete_crew(self, crew_id: str) -> dict:
        """Supprime un crew dans CrewAI Studio."""
        url = f"{self.url}/api/crews/{crew_id}"
        headers = {'Accept': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def delete_agent(self, agent_id: str) -> dict:
        """Supprime un agent dans CrewAI Studio."""
        url = f"{self.url}/api/agents/{agent_id}"
        headers = {'Accept': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
