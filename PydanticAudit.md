# Audit Pydantic V1 vs V2

## 1. Usage dans le projet DreamTeam

- **src/dreamteam/crew.py** : utilise `BaseModel` (via CrewAI Core), `@field_validator`, `@model_validator` (Pydantic V1).
- **src/dreamteam/tools/custom_tool.py** : `from pydantic import BaseModel, Field` (V1 patterns).

## 2. Usage dans les dépendances CrewAI

Coordination des modules internes chargé par CrewAI :

| Module                                                         | Version Pydantic                   |
|----------------------------------------------------------------|------------------------------------|
| crewai/task.py                                                 | V1 (`BaseModel`, `field_validator`, `model_validator`) |
| crewai/crew.py                                                 | V1 (`BaseModel`)                   |
| crewai/prompts.py                                              | V1                                 |
| crewai/tools/agent_tools.py                                    | V1                                 |
| crewai/tools/cache_tools.py                                    | Mixte (V2 `ConfigDict`, V1 `BaseModel`) |
| crewai/tasks/task_output.py                                    | V1                                 |
| crewai/process.py                                              | néglige les modèles (Enum)         |

## 3. Impacts constatés

- **Warning** "Mixing V1 models and V2 models (or constructs) is not supported" émis par Pydantic V2 lors de l'exécution.
- Risque de comportements imprévus ou incompatibilités futures entre validateurs V1 et V2.

## 4. Recommandations

1. **Planifier une migration vers Pydantic V2** :
   - Mettre à jour `CrewAgentExecutor` et les modèles CrewAI pour utiliser `ConfigDict` et V2 validators.
   - Remplacer `@field_validator` par `@model_validator` V2 (avec `mode="before"` ou `mode="after"`).
   - Valider l'absence de code V1 restant.

2. **Isolation temporaire** :
   - Filtrer le warning, mais documenter clairement la dette technique dans `DEVBOOK.md`.

3. **Audit régulier** :
   - Intégrer ce document dans la documentation interne pour suivre l’évolution.

---
*Établi le 2025-05-01*
