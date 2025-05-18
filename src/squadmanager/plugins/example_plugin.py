from squadmanager.connectors import ExternalPlugin


class ExamplePlugin(ExternalPlugin):
    """Plugin d'exemple renvoyant un statut ok et affichant un événement"""

    def __init__(self, config: dict):
        super().__init__(config)

    def health_check(self) -> dict:
        return {'example': 'ok'}

    def send_event(self, payload: dict) -> None:
        print(f"ExamplePlugin: sent event {payload}")
