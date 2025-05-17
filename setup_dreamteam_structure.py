#!/usr/bin/env python3
import os
import shutil
import sqlite3
import yaml

# Script de scaffolding pour créer la structure 'dreamteam' avec mémoire et subteams

def backup_config():
    backup_dir = os.path.join("backup", "old_config", "config")
    os.makedirs(backup_dir, exist_ok=True)
    for fname in [os.path.join("src", "dreamteam", "config", "agents.yaml"),
                  os.path.join("src", "dreamteam", "config", "tasks.yaml")]:
        if os.path.exists(fname):
            dst = os.path.join(backup_dir, os.path.basename(fname) + ".bak")
            shutil.copy(fname, dst)
            print(f"Backup de {fname} -> {dst}")


def create_dirs():
    paths = [
        os.path.join("src", "dreamteam", "config"),
        os.path.join("src", "dreamteam", "subteams", "marketing", "config"),
        os.path.join("src", "dreamteam", "tools"),
        os.path.join("src", "dreamteam", "memory"),
    ]
    for p in paths:
        os.makedirs(p, exist_ok=True)
        print(f"Création du dossier {p}")


def write_templates():
    # Config principale
    main_agents = """
DG_IA:
  role: "DG IA"
  goal: "Recevoir et prioriser les besoins métier du PDG humain"
  backstory: "Directeur Général IA, garant de la vision et coordination des équipes."

Cabinet_RH_IA:
  role: "Cabinet RH IA"
  goal: "Générer prompts pour agents et tâches"
  backstory: "Expert RH IA, configure agents et tasks dynamiquement."

Architecte_IA:
  role: "Architecte IA"
  goal: "Structurer l'arborescence et fichiers YAML"
  backstory: "Spécialiste organisation de projets IA."

Juriste_IA:
  role: "Juriste IA"
  goal: "Valider conformité éthique et légale"
  backstory: "Juriste IA, veille réglementaire et éthique."

Analyste_IA:
  role: "Analyste IA"
  goal: "Suivre performances des subteams"
  backstory: "Analyste de données IA, produit des rapports d'optimisation."

Documentaliste_IA:
  role: "Documentaliste IA"
  goal: "Gérer mémoire long-terme et archives"
  backstory: "Gardien de la mémoire du système pour auto-amélioration."

Conseil_IA:
  role: "Conseil IA"
  goal: "Évaluer décisions du DG et proposer axes d'amélioration"
  backstory: "Conseil stratégique IA pour évolution continue."

Chefs_de_projet:
  role: "Chefs de projet IA"
  goal: "Servir d'intermédiaire entre clients et IA"
  backstory: "Managers projet IA, communication client-projet."
"""
    agents_yaml = os.path.join("src", "dreamteam", "config", "agents.yaml")
    with open(agents_yaml, "w", encoding="utf-8") as f:
        f.write(main_agents)
    print(f"Écriture de {agents_yaml}")

    main_tasks = """
- name: generate_subteams
  agent: Cabinet_RH_IA
  description: Générer subteams selon pdg_input.yaml

- name: structure_project
  agent: Architecte_IA
  description: Créer arborescence et fichiers YAML

- name: validate_compliance
  agent: Juriste_IA
  description: Valider conformité des configs

- name: monitor_performance
  agent: Analyste_IA
  description: Suivre indicateurs des subteams

- name: archive_event
  agent: Documentaliste_IA
  description: Enregistrer événements dans history.jsonl et org_memory.db

- name: strategic_review
  agent: Conseil_IA
  description: Évaluer actions du DG et proposer améliorations
"""
    tasks_yaml = os.path.join("src", "dreamteam", "config", "tasks.yaml")
    with open(tasks_yaml, "w", encoding="utf-8") as f:
        f.write(main_tasks)
    print(f"Écriture de {tasks_yaml}")

    # Subteam marketing
    m_agents = """
Chef_projet_marketing:
  role: "Chef de projet marketing"
  goal: "Coordonner création de contenu IA"
  backstory: "Manager marketing IA, planifie campagnes."

Redacteur_IA:
  role: "Rédacteur IA"
  goal: "Rédiger articles et posts LinkedIn hebdomadaires"
  backstory: "Spécialiste contenu IA, expert en copywriting."
"""
    m_tasks = """
- name: write_article
  agent: Redacteur_IA
  description: Rédiger un article IA hebdomadaire

- name: post_linkedin
  agent: Redacteur_IA
  description: Publier l'article sur LinkedIn et analyser engagement
"""
    m_agents_yaml = os.path.join("src", "dreamteam", "subteams", "marketing", "config", "agents.yaml")
    with open(m_agents_yaml, "w", encoding="utf-8") as f:
        f.write(m_agents)
    print(f"Écriture de {m_agents_yaml}")
    m_tasks_yaml = os.path.join("src", "dreamteam", "subteams", "marketing", "config", "tasks.yaml")
    with open(m_tasks_yaml, "w", encoding="utf-8") as f:
        f.write(m_tasks)
    print(f"Écriture de {m_tasks_yaml}")

    # Memory
    mem_conf = """
memory_policy:
  default_level: normal
  override_by_event_type:
    subteam_created: important
    evaluation_dg: important
    task_completed: normal
"""
    mem_conf_path = os.path.join("src", "dreamteam", "memory", "config.yaml")
    with open(mem_conf_path, "w", encoding="utf-8") as f:
        f.write(mem_conf)
    print(f"Écriture de {mem_conf_path}")

    # Create history.jsonl and org_memory.db
    hist = os.path.join("src", "dreamteam", "memory", "history.jsonl")
    open(hist, "a").close()
    print(f"Création de {hist}")
    db = os.path.join("src", "dreamteam", "memory", "org_memory.db")
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        timestamp TEXT,
        event_type TEXT,
        data TEXT
    )''')
    conn.commit()
    conn.close()
    print(f"Création de {db}")

    # Tools
    tools = {
        "rh_prompt_generator.py": '''import yaml

def generate_prompts(pdg_input, output_dir):
    """Génère agents.yaml et tasks.yaml pour une subteam"""
    with open(pdg_input) as f:
        data = yaml.safe_load(f)
    # TODO: implémenter logique
    print("Prompts générés vers", output_dir)
''',
        "memory_logger.py": '''import json
import sqlite3

def log_event(event_type, data):
    """Ajoute un événement dans history.jsonl et org_memory.db"""
    evt = {"timestamp": data.get('timestamp'), "event_type": event_type, "data": data}
    # history.jsonl
    with open(os.path.join('src', 'dreamteam', 'memory', 'history.jsonl'), 'a') as f:
        f.write(json.dumps(evt) + '\n')
    # org_memory.db
    conn = sqlite3.connect(os.path.join('src', 'dreamteam', 'memory', 'org_memory.db'))
    c = conn.cursor()
    c.execute("INSERT INTO events VALUES (?, ?, ?)", (evt['timestamp'], evt['event_type'], json.dumps(evt)))
    conn.commit()
    conn.close()
    print("Événement enregistré:", event_type)
'''    }
    for name, code in tools.items():
        path = os.path.join("src", "dreamteam", "tools", name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"Écriture de {path}")

    # Entrées YAML
    pdg = """
agents_needed: marketing
clients: []
"""
    with open(os.path.join("src", "dreamteam", "pdg_input.yaml"), "w", encoding="utf-8") as f:
        f.write(pdg)
    print("Écriture de pdg_input.yaml")
    client = """
client_request: "Article IA optimisé SEO"
"""
    with open(os.path.join("src", "dreamteam", "client_input.yaml"), "w", encoding="utf-8") as f:
        f.write(client)
    print("Écriture de client_input.yaml")


def main():
    backup_config()
    create_dirs()
    write_templates()
    print("Structure DreamTeam générée avec succès.")

if __name__ == "__main__":
    main()
