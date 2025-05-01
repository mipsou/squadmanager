import crewai
import yaml
from pathlib import Path
from typing import List
from langchain.chat_models.ollama import ChatOllama
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Mixing V1 models and V2 models*")

# CrewAI core imports
Agent = getattr(crewai, 'Agent', None)
Crew = getattr(crewai, 'Crew', None)
Process = getattr(crewai, 'Process', None)
Task = getattr(crewai, 'Task', None)
CrewBase = getattr(crewai, 'CrewBase', lambda cls: cls)

# Decorator stubs
_local_agent = getattr(crewai, 'agent', None)
agent = _local_agent if callable(_local_agent) else (lambda fn: fn)
_local_crew = getattr(crewai, 'crew', None)
crew = _local_crew if callable(_local_crew) else (lambda fn: fn)
_local_task = getattr(crewai, 'task', None)
task = _local_task if callable(_local_task) else (lambda fn: fn)
_local_before_kickoff = getattr(crewai, 'before_kickoff', None)
before_kickoff = _local_before_kickoff if callable(_local_before_kickoff) else (lambda fn: fn)

# BaseAgent import fallback
try:
    from crewai.agents.agent_builder.base_agent import BaseAgent
except ImportError:
    BaseAgent = object

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Dreamteam():
    """Dreamteam crew"""

    # Stub pour détecter une nouvelle demande de projet
    def has_new_project_request(self) -> bool:
        # TODO: implémenter la vérification (DB, fichier, etc.)
        return False

    def get_next_request(self) -> dict:
        # TODO: récupérer les paramètres du prochain projet
        raise NotImplementedError("Implement project request retrieval")

    @before_kickoff
    def standby(self):
        import time
        print(" En attente d'une demande de création de crew…")
        while not self.has_new_project_request():
            time.sleep(5)
        params = self.get_next_request()
        # Injection des paramètres dans les tâches de génération de CDC
        for name in ["draft_prompt", "review_prompt", "finalize_prompt"]:
            self.tasks_config[name]["parameters"].update(params)

    def __init__(self):
        # Chargement des configs agents et tasks
        config_dir = Path(__file__).parent / "config"
        self.agents_config = yaml.safe_load((config_dir / "agents.yaml").read_text())
        self.tasks_config = yaml.safe_load((config_dir / "tasks.yaml").read_text())
        # Bypass validation: définir openai_api_key ou llm selon le provider
        for cfg in self.agents_config.values():
            if cfg.get("provider") == "ollama":
                # Utiliser ChatOllama pour les modèles Ollama
                cfg["llm"] = ChatOllama(
                    model_name=cfg.get("model"),
                    base_url=cfg.get("base_url"),
                )
            else:
                cfg.setdefault("openai_api_key", "")
        # Instanciation dynamique des agents et tâches
        self.agents = []
        self.agents_by_name = {}
        for name in self.agents_config.keys():
            agent_instance = getattr(self, name)()
            self.agents.append(agent_instance)
            self.agents_by_name[name] = agent_instance
        self.tasks = [getattr(self, name)() for name in self.tasks_config.keys()]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    # Agents defined in config
    @agent
    def superviseur(self) -> Agent:
        cfg = self.agents_config['superviseur']
        return Agent(**cfg, verbose=True)

    @agent
    def chef_de_projet(self) -> Agent:
        cfg = self.agents_config['chef_de_projet']
        return Agent(**cfg, verbose=True)

    @agent
    def prompteur(self) -> Agent:
        cfg = self.agents_config['prompteur']
        return Agent(**cfg, verbose=True)

    @agent
    def qa(self) -> Agent:
        cfg = self.agents_config['qa']
        return Agent(**cfg, verbose=True)

    @agent
    def analyste(self) -> Agent:
        cfg = self.agents_config['analyste']
        return Agent(**cfg, verbose=True)

    @agent
    def documentaliste(self) -> Agent:
        cfg = self.agents_config['documentaliste']
        return Agent(**cfg, verbose=True)

    @agent
    def directeur_general(self) -> Agent:
        cfg = self.agents_config['directeur_general']
        return Agent(**cfg, verbose=True)

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    # Tâches de prompt_generation définies dans config
    @task
    def draft_prompt(self) -> Task:
        cfg = self.tasks_config['draft_prompt']
        agent_name = cfg.get('agent')
        agent = self.agents_by_name.get(agent_name)
        return Task(
            description=cfg['description'],
            agent=agent,
            tools=cfg.get('tools', []),
            **cfg.get('parameters', {})
        )

    @task
    def review_prompt(self) -> Task:
        cfg = self.tasks_config['review_prompt']
        agent_name = cfg.get('agent')
        agent = self.agents_by_name.get(agent_name)
        return Task(
            description=cfg['description'],
            agent=agent,
            tools=cfg.get('tools', []),
            **cfg.get('parameters', {})
        )

    @task
    def finalize_prompt(self) -> Task:
        cfg = self.tasks_config['finalize_prompt']
        agent_name = cfg.get('agent')
        agent = self.agents_by_name.get(agent_name)
        return Task(
            description=cfg['description'],
            agent=agent,
            tools=cfg.get('tools', []),
            **cfg.get('parameters', {})
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Dreamteam crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
