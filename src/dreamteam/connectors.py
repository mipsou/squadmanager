from abc import ABC, abstractmethod


class ExternalPlugin(ABC):
    """Interface pour les plugins externes dreamteam"""

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def health_check(self) -> dict:
        """Vérifie la santé du service externe. Retourne un dict JSON-like."""
        pass

    @abstractmethod
    def send_event(self, payload: dict) -> None:
        """Envoie un événement au service externe."""
        pass
