from squadmanager.connectors import ExternalPlugin


class ExamplePlugin(ExternalPlugin):
    """Plugin d'exemple pour démontrer le système de plugins."""

    def health_check(self) -> dict:
        """Retourne un status simulé."""
        return {"example": "ok"}

    def send_event(self, payload: dict) -> None:
        """Reçoit un payload et simule un envoi (log)."""
        print(f"ExamplePlugin: sent event {payload}")
