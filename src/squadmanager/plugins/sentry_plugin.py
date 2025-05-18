import os
import sentry_sdk
from squadmanager.connectors import ExternalPlugin


class SentryPlugin(ExternalPlugin):
    """Sentry plugin pour initialisation et envoi d'événements."""

    def __init__(self, config: dict):
        super().__init__(config)
        dsn = config.get('dsn') or os.getenv('CREWAI_SENTRY_DSN')
        if not dsn:
            raise ValueError('DSN Sentry est manquant')
        sentry_sdk.init(dsn=dsn)
        self.dsn = dsn

    def health_check(self) -> dict:
        return {'sentry': 'initialized'}

    def send_event(self, payload: dict) -> None:
        if 'exception' in payload:
            sentry_sdk.capture_exception(payload['exception'])
        else:
            sentry_sdk.capture_message(str(payload))
