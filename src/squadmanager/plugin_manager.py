import importlib.metadata as _metadata
from typing import Dict, Any
from squadmanager.connectors import ExternalPlugin


class PluginManager:
    """Gère le chargement dynamique des plugins externes via entry_points."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.plugins: Dict[str, ExternalPlugin] = {}
        self.load_plugins()

    def load_plugins(self) -> None:
        """Charge tous les plugins déclarés sous le groupe 'squadmanager.plugins'."""
        try:
            eps = _metadata.entry_points(group="squadmanager.plugins")
        except TypeError:
            # Pour compatibilité Python <3.10
            eps = _metadata.entry_points().get("squadmanager.plugins", [])
        for ep in eps:
            plugin_cls = ep.load()
            plugin_config = self.config.get(ep.name, {})
            try:
                plugin = plugin_cls(plugin_config)
            except Exception:
                # Skip plugin if init fails (missing config)
                continue
            self.plugins[ep.name] = plugin

    def list_plugins(self) -> list[str]:
        """Retourne la liste des plugins chargés."""
        return list(self.plugins.keys())

    def get_plugin(self, name: str) -> ExternalPlugin:
        """Retourne le plugin par nom."""
        return self.plugins.get(name)
