[![CI](https://img.shields.io/github/actions/workflow/status/mipsou/squadmanager/ci.yml?branch=main&style=flat-square&color=blue)](https://github.com/mipsou/squadmanager/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/mipsou/squadmanager?style=flat-square&color=brightgreen)](https://github.com/mipsou/squadmanager/releases)
[![PyPI version](https://img.shields.io/pypi/v/squadmanager?style=flat-square&color=orange)](https://pypi.org/project/squadmanager/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)](https://opensource.org/licenses/Apache-2.0)
[![Docs](https://img.shields.io/badge/docs-crewAI-blue?style=flat-square)](https://docs.crewai.com)

 

# Squadmanager Crew — Multi-Agent AI Orchestration

## 🇫🇷 Français
Un modèle Full Scale CrewAI, pensé pour être à la fois complet et facile d’utilisation par chacun.

Squadmanager Crew est un framework open-source Python permettant d’orchestrer un système multi-agents IA complet.
Basé sur CrewAI, il propose l’intégration native de la gestion de la mémoire, des workflows collaboratifs et un écosystème de plugins modulaires.
Parfait pour déployer rapidement des applications IA évolutives et performantes.

## 🇬🇧 English
Full Scale CrewAI model: a new-generation framework that is comprehensive, powerful, and easy to use for everyone.

Squadmanager Crew is an open-source Python framework for orchestrating a complete multi-agent AI system.
Built on CrewAI, it provides native memory management, collaborative workflows, and a modular plugin ecosystem.
Perfect for quickly deploying scalable, high-performance AI applications.

## Table of Contents

- 🚀 [Installation](#installation)
- ⚙️ [Usage](#usage)
- 📖 [Memory System Concepts](#memory-system-concepts)
- 🖥️ [CrewAI Studio Integration](#installation-crewai-studio)
- 🔌 [Plugins](#plugins)
- 🧪 [Testing](#testing)
- 💖 [Contributing](#contributing)
- 📄 [License](#license)
- 📋 [Gestion de projet](#gestion-de-projet)
- 📞 [Contact](#contact)
- 🚨 [Dépannage](#dépannage)

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install the extras tools of CrewAI and then uv:

```bash
pip install "crewai[tools]>=0.11.2,<0.12.0"
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
uv install
```

## Usage
Pour afficher le prototype structuré du Cahier des Charges :
```bash
squadmanager demo
# ou pour le développement
python -m squadmanager.cli demo
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/squadmanager/config/agents.yaml` to define your agents
- Modify `src/squadmanager/config/tasks.yaml` to define your tasks
- Modify `src/squadmanager/config/memory.yaml` to configure external memory (short_term, long_term, entity)
- Modify `src/squadmanager/crew.py` to add your own logic, tools and specific args
- Modify `src/squadmanager/main.py` to add custom inputs for your agents and tasks

## Installation CrewAI Studio Backend
Pour configurer et lancer le **backend REST** de CrewAI Studio :

1. Installer le package ou cloner le dépôt :
   - Depuis PyPI :
     ```bash
     pip install crewai-studio-backend
     ```
   - Ou cloner et installer :
     ```bash
     git clone https://github.com/crew-ai/crewai-studio-backend.git
     cd crewai-studio-backend
     pip install -r requirements.txt
     ```

2. Lancer le serveur REST via Uvicorn :
   ```bash
   uvicorn crewai_studio.main:app --reload --port 8000
   ```

3. Vérifier le service :
   ```bash
   curl http://localhost:8000/api/status
   ```

4. Configurer la CLI :
   ```bash
   export CREWAI_STUDIO_URL=http://localhost:8000  # Windows : set CREWAI_STUDIO_URL=...
   ```

5. Importer et lister un crew :
   ```bash
   squadmanager studio import path/to/squadmanagerAI.yml
   squadmanager studio list
   ```
6. Ouvrir l'UI de CrewAI Studio :
   ```bash
  squadmanager studio --open
   ```
7. Lancer l'interface locale de CrewAI Studio :
   ```bash
  squadmanager studio serve
   ```
8. Arrêter l'interface locale de CrewAI Studio :
   ```bash
  squadmanager studio stop
   ```
9. Redémarrer l'interface locale de CrewAI Studio :
   ```bash
  squadmanager studio restart
   ```

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
squadmanager run [--once]
```

This command initializes the squadmanager Crew, assembling the agents and assigning them tasks as defined in your configuration.

## Running the Flow

Pour exécuter le flow squadmanager via CrewAI Flows, utilisez :

```bash
squadmanager flow [--topic <topic>] [--year <year>]
```

### Commandes mémoire

```bash
squadmanager memory-show
squadmanager memory-stats
squadmanager memory-apply-policy [--ttl-days <jours>] [--max-events <nombre>]
```

- `memory-show` : Affiche l'historique des événements (JSONL).
- `memory-stats` : Affiche le nombre d'événements et les tables SQLite.
- `memory-apply-policy` : Applique la politique d'éviction (TTL en jours, nombre max d'événements).

### Testing
Pour exécuter les tests unitaires et d'intégration, utilisez :

```bash
squadmanager test
```

Pour vérifier les prérequis puis lancer les tests CrewAI, utilisez :

```bash
squadmanager crewai_test
```

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

### Memory System Concepts
La documentation complète est disponible ici : [![Docs](https://img.shields.io/badge/docs-memory-brightgreen?style=flat-square)](https://docs.crewai.com/concepts/memory)

Ce document couvre les sections suivantes :
1. Introduction to Memory Systems in CrewAI
2. Memory System Components (RAG, ShortTermMemory, LongTermMemory, EntityMemory, ExternalMemory)
3. How Memory Systems Empower Agents
4. Implementing Memory in Your Crew (activation, embedders, instances custom)
5. Configuration Examples (Basic Memory Configuration, Custom Storage)
6. Security Considerations
7. External Memory (Basic Usage with Mem0, Custom Storage)
8. Additional Embedding Providers

Pour plus de détails et guider votre implémentation, consultez directement la doc officielle.

## Configurer la mémoire externe
Placez un fichier `config/memory.yaml` dans `src/squadmanager/` contenant :
```yaml
short_term_memory:
  storage:
    embedder_config:
      provider: openai
      config:
        model: text-embedding-3-small
    type: short_term
    path: memory/short_term

long_term_memory:
  storage:
    db_path: memory/org_memory.db

entity_memory:
  storage:
    embedder_config:
      provider: openai
      config:
        model: text-embedding-3-small
    type: entity
    path: memory/entity
```
Ensuite, instanciez votre crew :
```python
from squadmanager.crew import squadmanager

dt = squadmanager(config_path='src/squadmanager/config')
crew = dt.crew()
crew.kickoff()
```

## Workflow Global : Fonctionnement complet du système IA

Le cycle standard :
1. Expression du besoin  
   - **PDG humain** via `pdg_input.yaml`  
   - **Client** (humain ou IA) via `client_input.yaml`  
   - **Chef de projet** lit et reformule la demande au **DG IA**
2. Traitement stratégique  
   - **DG IA** analyse la demande et décide de créer une nouvelle subteam, étendre une équipe existante ou réutiliser des ressources internes
3. Recrutement IA  
   - **Cabinet RH IA** génère les prompts (rôle, goal, backstory) et les tâches (description, expected_output)
4. Structuration  
   - **Architecte IA** crée les fichiers YAML et dossiers dans `/subteams/{nom}/config/`
5. Validation  
   - **Juriste IA** valide la syntaxe, la clarté et la cohérence des rôles et tâches
6. Historisation  
   - **Documentaliste IA** logue l'événement dans `memory/history.jsonl` et l'injecte selon la politique dans `memory/org_memory.db`
7. Exécution des tâches  
   - **Subteam** exécute les tâches via CrewAI  
   - **Analyste IA** suit les performances et l'efficacité
8. Évaluation  
   - **Conseil IA** évalue les décisions du DG, les résultats et leur impact, puis publie un rapport dans `improvements.log`
9. Amélioration continue  
   - **DG IA** restructure l’organisation ou déclenche une nouvelle itération  
   - **Documentaliste IA** trace chaque évolution

## Dépannage

En cas de problème avec le bootstrap ou le lancement de la CLI :

1. Lire les derniers logs :
   ```powershell
   Get-Content .\bootstrap.log -Tail 100
   ```
2. Fermer/terminer manuellement les processus bloquants :
   ```powershell
   Get-Process squadmanager, uv, uvicorn -ErrorAction SilentlyContinue | Stop-Process -Force
   ```
3. Réinstaller le projet en editable :
   ```powershell
   .\.venv\Scripts\Activate.ps1
   pip install -e .
   ```
4. Relancer la CLI :
   ```powershell
   squadmanager run --once
   ```
5. En fallback, utiliser `unlock_module.py` :
   ```powershell
   python unlock_module.py
   squadmanager run --once
   ```
6. Ajouter un test TDD `tests/test_bootstrap.py` pour valider que `python bootstrap_run.py` renvoie `exit code 0`.

## Développement de plugins

squadmanager supporte un système de plugins via le groupe d’entry points `squadmanager.plugins`.

Pour créer votre propre plugin :

1. Créez un nouveau paquet Python (par exemple `squadmanager-plugin-monplugin`).
2. Implémentez une classe héritant de `squadmanager.connectors.ExternalPlugin` :
```python
from squadmanager.connectors import ExternalPlugin

class MonPlugin(ExternalPlugin):
    def health_check(self) -> dict:
        """Vérifie la santé du service externe"""
        # Retournez un dict JSON-like
        return {"monplugin": "ok"}

    def send_event(self, payload: dict) -> None:
        """Envoie un événement au service externe"""
        # Votre logique ici
        print(f"MonPlugin envoi : {payload}")
```
3. Dans le `pyproject.toml` de votre plugin, déclarez l’entry point :
```toml
[project.entry-points."squadmanager.plugins"]
monplugin = "monpackage.module:MonPlugin"
```
4. Publiez et installez votre plugin :
```bash
pip install squadmanager-plugin-monplugin
```
5. Vérifiez la détection des plugins :
```python
from squadmanager.plugin_manager import PluginManager
mgr = PluginManager()
print(mgr.list_plugins())  # ex. ['example', 'monplugin']
```

**Plugins intégrés :**
- `example` : plugin d’exemple fourni pour démarrer.

## Understanding Your Crew

The squadmanager Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Gestion de projet

Organisez et suivez l’avancement avec **GitHub Projects** :
- Board principal : https://github.com/mipsou/squadmanager/projects
- Colonnes : *Backlog*, *In Progress*, *Done*
- Liez issues/PRs aux cartes, utilisez *labels* et *milestones*
- Mettez à jour le board régulièrement pour garantir la visibilité

## Contact
Pour toute question, voir [mon profil GitHub](https://github.com/mipsou).
