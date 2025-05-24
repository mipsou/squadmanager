# Changelog

## [0.3.0] - 2025-05-24

### Added
- Commandes `stop` et `restart` pour l'interface Streamlit de CrewAI Studio
- Commandes CLI mémoire (show, stats, apply-policy, reset) en top-level
- Gestion des plugins plantant à l'init (skip)

### Changed
- Bump de version vers 0.3.0

### Fixed
- Tests CLI mémoire désormais passants

## [0.4.0] - 2025-05-24

### Added
- Commande `spec` pour structurer le CDC depuis fichier et en mode interactif
- Formulaire `spec_template.md` ajouté comme exemple pré-rempli

### Changed
- Bump de version vers 0.4.0

### Testing
- Ajout des tests TDD pour `spec` dans `tests/test_cli_spec.py`
