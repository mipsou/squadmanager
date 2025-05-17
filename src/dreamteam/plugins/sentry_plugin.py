import os
import sentry_sdk
from dreamteam.connectors import ExternalPlugin


class SentryPlugin(ExternalPlugin):
    """Plugin pour intégrer Sentry via sentry-sdk."""

    def __init__(self, config: dict):
        super().__init__(config)
        dsn = config.get('dsn') or os.getenv('CREWAI_SENTRY_DSN')
        if not dsn:
            raise ValueError("Le DSN Sentry est manquant. Définir CREWAI_SENTRY_DSN ou passer 'dsn' en config.")
        sentry_sdk.init(dsn=dsn)

    def health_check(self) -> dict:
        """Vérifie l'initialisation de Sentry."""
        return {"sentry": "initialized"}

    def send_event(self, payload: dict) -> None:
        """Envoie un événement ou exception à Sentry."""
        exc = payload.get('exception')
        if exc:
            sentry_sdk.capture_exception(exc)
        else:
            sentry_sdk.capture_message(str(payload))
