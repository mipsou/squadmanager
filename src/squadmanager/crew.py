import warnings
warnings.filterwarnings("ignore", message="Mixing V1 models and V2 models")

import yaml
from pathlib import Path

# Optional support for Ollama models
try:
    from langchain.chat_models.ollama import ChatOllama
except ImportError:
    ChatOllama = None

import crewai
from crewai import Agent, Crew, Process, Task

# Stubs pour wrapper CrewAI
CrewBase = lambda cls: cls
agent = lambda fn: fn
crew = lambda fn: fn
task = lambda fn: fn

# Lifecycle decorators
try:
    from crewai import before_kickoff, after_kickoff
except ImportError:
    def before_kickoff(fn): return fn
    def after_kickoff(fn): return fn

# BaseAgent fallback
try:
    from crewai.agents.agent_builder.base_agent import BaseAgent
except ImportError:
    BaseAgent = object

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class squadmanager():
    """squadmanager crew"""

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

    def __init__(self, config_path: str = None):
        # Chargement des configs agents et tasks
        if config_path:
            config_dir = Path(config_path)
        else:
            config_dir = Path(__file__).parent / "config"
        # Charger config mémoire externe
        self.memory_config = {}
        memory_file = config_dir / "memory.yaml"
        if memory_file.exists():
            self.memory_config = yaml.safe_load(memory_file.read_text())
        self.agents_config = yaml.safe_load((config_dir / "agents.yaml").read_text())
        raw_tasks = yaml.safe_load((config_dir / "tasks.yaml").read_text())
        # Transformer la liste de tâches en dictionnaire {name: config}
        self.tasks_config = {task['name']: task for task in raw_tasks}
        # Bypass validation: définir openai_api_key ou llm selon le provider
        for cfg in self.agents_config.values():
            if cfg.get("provider") == "ollama" and ChatOllama:
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
        # Instancier uniquement les tâches dont la méthode est définie
        self.tasks = []
        for name in self.tasks_config.keys():
            if hasattr(self, name):
                self.tasks.append(getattr(self, name)())
            else:
                warnings.warn(f"Méthode de tâche '{name}' non implémentée, ignorée.")

    # Méthodes agents définies manuellement
    @agent
    def dg_ia(self) -> Agent:
        cfg = self.agents_config['dg_ia']
        return Agent(**cfg, verbose=True)
    @agent
    def cabinet_rh(self) -> Agent:
        cfg = self.agents_config['cabinet_rh']
        return Agent(**cfg, verbose=True)
    @agent
    def architecte_ia(self) -> Agent:
        cfg = self.agents_config['architecte_ia']
        return Agent(**cfg, verbose=True)
    @agent
    def juriste_ia(self) -> Agent:
        cfg = self.agents_config['juriste_ia']
        return Agent(**cfg, verbose=True)
    @agent
    def analyste_ia(self) -> Agent:
        cfg = self.agents_config['analyste_ia']
        return Agent(**cfg, verbose=True)
    @agent
    def documentaliste_ia(self) -> Agent:
        cfg = self.agents_config['documentaliste_ia']
        return Agent(**cfg, verbose=True)
    @agent
    def conseil_ia(self) -> Agent:
        cfg = self.agents_config['conseil_ia']
        return Agent(**cfg, verbose=True)
    @agent
    def chef_de_projet(self) -> Agent:
        cfg = self.agents_config['chef_de_projet']
        return Agent(**cfg, verbose=True)

    # Méthodes tasks définies manuellement
    @task
    def draft_prompt(self) -> Task:
        cfg = self.tasks_config['draft_prompt']
        agent_inst = self.agents_by_name[cfg['agent']]
        return Task(
            description=cfg['description'],
            agent=agent_inst,
            tools=cfg.get('tools', []),
            **cfg.get('parameters', {})
        )
    @task
    def review_prompt(self) -> Task:
        cfg = self.tasks_config['review_prompt']
        agent_inst = self.agents_by_name[cfg['agent']]
        return Task(
            description=cfg['description'],
            agent=agent_inst,
            tools=cfg.get('tools', []),
            **cfg.get('parameters', {})
        )
    @task
    def finalize_prompt(self) -> Task:
        cfg = self.tasks_config['finalize_prompt']
        agent_inst = self.agents_by_name[cfg['agent']]
        return Task(
            description=cfg['description'],
            agent=agent_inst,
            tools=cfg.get('tools', []),
            **cfg.get('parameters', {})
        )

    def crew(self) -> Crew:
        """Creates the squadmanager crew"""
        crew_kwargs = {
            "agents": self.agents,
            "tasks": self.tasks,
            "process": Process.sequential,
            "verbose": True,
            "memory": True
        }
        # Injection mémoire externe si configurée
        mc = getattr(self, "memory_config", {})
        if mc:
            from crewai.memory import ShortTermMemory, LongTermMemory, EntityMemory
            from crewai.memory.storage.rag_storage import RAGStorage
            from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
            if mc.get("short_term_memory"):
                st_conf = mc["short_term_memory"].get("storage", {})
                crew_kwargs["short_term_memory"] = ShortTermMemory(storage=RAGStorage(**st_conf))
            if mc.get("long_term_memory"):
                lt_conf = mc["long_term_memory"].get("storage", {})
                crew_kwargs["long_term_memory"] = LongTermMemory(storage=LTMSQLiteStorage(**lt_conf))
            if mc.get("entity_memory"):
                em_conf = mc["entity_memory"].get("storage", {})
                crew_kwargs["entity_memory"] = EntityMemory(storage=RAGStorage(**em_conf))
        return Crew(**crew_kwargs)

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
