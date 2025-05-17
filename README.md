[![CI](https://img.shields.io/github/actions/workflow/status/mipsou/dreamteam/ci.yml?branch=main&style=flat-square&color=blue)](https://github.com/mipsou/dreamteam/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/mipsou/dreamteam?style=flat-square&color=brightgreen)](https://github.com/mipsou/dreamteam/releases)
[![PyPI version](https://img.shields.io/pypi/v/dreamteam?style=flat-square&color=orange)](https://pypi.org/project/dreamteam/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)](https://opensource.org/licenses/Apache-2.0)
[![Docs](https://img.shields.io/badge/docs-crewAI-blue?style=flat-square)](https://docs.crewai.com)

# Dreamteam Crew
+ *Orchestrate your AI crew with ease.*  
+
+ ---  
+
+ ## Table of Contents  
+ - 🚀 [Installation](#installation)  
+ - ⚙️ [Usage](#usage)  
+ - 📖 [Memory System Concepts](#memory-system-concepts)  
+ - 🖥️ [CrewAI Studio Integration](#crewai-studio-integration)  
+ - 🔌 [Plugins](#plugins)  
+ - 🧪 [Testing](#testing)  
+ - 💖 [Contributing](#contributing)  
+ - 📄 [License](#license)  
+
+ ---
Welcome to the Dreamteam Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/dreamteam/config/agents.yaml` to define your agents
- Modify `src/dreamteam/config/tasks.yaml` to define your tasks
- Modify `src/dreamteam/config/memory.yaml` to configure external memory (short_term, long_term, entity)
- Modify `src/dreamteam/crew.py` to add your own logic, tools and specific args
- Modify `src/dreamteam/main.py` to add custom inputs for your agents and tasks

## Installation CrewAI Studio

Pour configurer et lancer le Studio :

1. Cloner le dépôt CrewAI-Studio et se placer dedans  
   ```bash
   git clone https://github.com/mipsou/CrewAI-Studio.git
   cd CrewAI-Studio
   ```
2. Créer et activer l’environnement conda (via `environment.yml`) :  
   ```bash
   conda env create -f environment.yml
   conda activate crewai-studio
   pip install uv
   ```
3. Lancer le script d’installation pour configurer les caches sur D:  
   ```powershell
   .\install_venv.bat
   ```
4. Démarrer l’environnement et Playwright :  
   ```powershell
   .\run_venv.bat
   ```

> Les variables d’environnement définies dans ces scripts  
> (`PIP_CACHE_DIR`, `XDG_CACHE_HOME`, `PLAYWRIGHT_BROWSERS_PATH`)  
> pointent vers `D:\Scripts\CrewAI-Studio\.cache` pour préserver l’espace sur C:.

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
dreamteam run [--once]
```

This command initializes the DreamTeam Crew, assembling the agents and assigning them tasks as defined in your configuration.

## Running the Flow

Pour exécuter le flow Dreamteam via CrewAI Flows, utilisez :

```bash
dreamteam flow [--topic <topic>] [--year <year>]
```

### Commandes mémoire

```bash
dreamteam memory-show
dreamteam memory-stats
dreamteam memory-apply-policy [--ttl-days <jours>] [--max-events <nombre>]
```

- `memory-show` : Affiche l'historique des événements (JSONL).
- `memory-stats` : Affiche le nombre d'événements et les tables SQLite.
- `memory-apply-policy` : Applique la politique d'éviction (TTL en jours, nombre max d'événements).

### Testing
Pour exécuter les tests unitaires et d'intégration, utilisez :

```bash
dreamteam test
```

Pour vérifier les prérequis puis lancer les tests CrewAI, utilisez :

```bash
dreamteam crewai_test
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
Placez un fichier `config/memory.yaml` dans `src/dreamteam/` contenant :
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
from dreamteam.crew import Dreamteam

dt = Dreamteam(config_path='src/dreamteam/config')
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

## Développement de plugins

DreamTeam supporte un système de plugins via le groupe d’entry points `dreamteam.plugins`.

Pour créer votre propre plugin :

1. Créez un nouveau paquet Python (par exemple `dreamteam-plugin-monplugin`).
2. Implémentez une classe héritant de `dreamteam.connectors.ExternalPlugin` :
```python
from dreamteam.connectors import ExternalPlugin

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
[project.entry-points."dreamteam.plugins"]
monplugin = "monpackage.module:MonPlugin"
```
4. Publiez et installez votre plugin :
```bash
pip install dreamteam-plugin-monplugin
```
5. Vérifiez la détection des plugins :
```python
from dreamteam.plugin_manager import PluginManager
mgr = PluginManager()
print(mgr.list_plugins())  # ex. ['example', 'monplugin']
```

**Plugins intégrés :**
- `example` : plugin d’exemple fourni pour démarrer.

## Understanding Your Crew

The DreamTeam Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the Dreamteam Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Guide d’installation officiel](https://docs.crewai.com/installation)
- [Chat GPT dédié CrewAI](https://chat.g.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.

## Contact
Pour toute question, voir [mon profil GitHub](https://github.com/mipsou).
