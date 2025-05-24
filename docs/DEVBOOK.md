# DEVBOOK.md

*Pousser sur Git sert de sauvegarde (backup sur le dépôt)*

## Jalons d'Avancement
*Ce document consigne les jalons d'avancement du projet.*

- **2025-04-28T23:33:24+02:00** : Création de `DEVBOOK.md` et documentation de la création de `CDC.md` avec la structure hiérarchique CrewIA.
- **2025-04-28T23:37:11+02:00** : Mise à jour de `CDC.md` : ajout des sections Processus de Création et d'Ajustement d'Équipe et Flexibilité et Adaptabilité.
- **2025-04-28T23:41:55+02:00** : Ajout de la section Rôles et Responsabilités de squadmanager dans `CDC.md`.
- **2025-04-28T23:46:18+02:00** : Mise à jour de `CDC.md` : chaque projet disposera d'un CDC dédié.
- **2025-04-28T23:52:03+02:00** : Correction dans `CDC.md` des Principes d'Agent : lecture systématique de `DEVBOOK.md` et `CDC.md` rétablie.
- **2025-04-28T23:53:51+02:00** : Renommage de la section pour consigner les jalons d'avancement.
- **2025-04-28T23:57:05+02:00** : Ajout de la section Processus de Traduction IA du CDC dans `CDC.md`.
- **2025-04-29T00:05:00+02:00** : Création des Crews via CLI CrewAI.
- **2025-05-01T06:00:35+02:00** : Ajout de l’audit Pydantic V1 vs V2 dans `PydanticAudit.md` et plan d’action défini.
- **2025-05-17T17:34:46+02:00** : Création d'un backup complet du code et mise à jour des tâches DEVBOOK.md
- **2025-05-17T17:56:08+02:00** : Implémentation du workflow étoile pour la mémoire externe
- **2025-05-17T19:46:02+02:00** : Release & maintenance (tests PyPI, CLI --version, tag v0.1.0)
- **2025-05-17T19:51:30+02:00** : Monitoring & Observabilité (Sentry, Prometheus/Grafana, tests de charge, alertes CI)
- **2025-05-17T21:15:20+02:00** : Plugin Dev Kit (example plugin, documentation, plugin manager)
- **2025-05-24T16:52:45+02:00** : Bump de version 0.3.0, création de CHANGELOG et commit release
- **2025-05-24T21:02:10+02:00** : Bump de version 0.4.0, implémentation `spec` & `demo`

## Tâches
- [x] Audit Pydantic V1 vs V2 (PydanticAudit.md)
- [x] Création de l'issue GitHub “Plan de migration vers Pydantic V2” (#1)
- [x] Migration du schéma `MyCustomToolInput` vers Pydantic V2
- [x] Création de la branche `pydantic-v2-migration`
- [x] Migration des modèles Pydantic V1 internes de crewai (CrewAgentExecutor, Task, prompts)
- [x] Refactorisation des validateurs V1 en V2 (`@field_validator` → `@model_validator`)
- [x] Mise à jour des tests unitaires et e2e
- [x] Validation finale et documentation complète
- [x] Stabilisation du CLI (tests et parsing)
- [x] Implémentation et tests du Flow squadmanager
- [x] Implémentation du système de mémoire et persistance
- [x] Mise à jour de la documentation et configuration OS spécifique
- [x] Configuration CI/CD et packaging
- [x] Release & maintenance
- [x] Example plugin Dev Kit (exemple, documentation, plugin manager)
- [x] Créer plugin Sentry
- [x] Créer plugin Studio
- [x] Implémentation des commandes CLI plugin (list, health, send)
- [x] Tests unitaires plugin Studio (import_crew, list_crews)
- [x] Tests d'intégration plugin Studio (fixture uvicorn, import & list)
- [x] Mise à jour README pour backend REST CrewAI Studio
- [ ] Créer plugin Prometheus (non applicable, pas d'infra)
- [ ] Intégrer Sentry pour logs/erreurs
- [ ] Mettre en place métriques Prometheus/Grafana
- [ ] Rédiger tests de charge basiques
- [ ] Définir alertes CI (coverage, performances)

## Tâches v0.4.0
- [x] Implémentation commande `spec` interactive et tests TDD
- [x] Implémentation commande `demo` et tests TDD
- [x] Ajout de `__main__.py` pour exécution en module
- [x] Lock des dépendances (`requirements.txt`)
- [x] Mise à jour CI (install via requirements.txt, lint, format, tests, build, smoke test)
- [x] Mise à jour README (Installation, Usage, spec, demo)
- [x] Création de la PR #22 sur GitHub
- [x] Smoke test demo dans CI
- [x] Exemples specs : ChatBot IA, Gestion Inventaire IA, Recommandation IA
- [ ] Prototypage EventBus multi-agents IA
- [ ] Tests flow asynchrone via EventBusMock
- [ ] Plugin Prometheus
- [ ] Intégration Sentry (logs/erreurs)
- [ ] Tests de charge basiques
- [ ] Alertes CI (coverage, performances)
