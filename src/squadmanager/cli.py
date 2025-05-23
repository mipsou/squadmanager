import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from squadmanager.core import squadmanager
from squadmanager.flow import DreamteamFlow, DreamteamState
import json
import sqlite3
from squadmanager.memory import MemoryManager
from squadmanager.memory_policy import MemoryPolicy
from importlib.metadata import version as _version, PackageNotFoundError
import requests
import webbrowser
from pathlib import Path
import yaml
from squadmanager.plugin_manager import PluginManager
from argparse import RawTextHelpFormatter

try:
    __version__ = _version('squadmanager')
except PackageNotFoundError:
    __version__ = '0.0.0'

def auto_detect_studio_url(ports=None):
    """Detecte localement un service CrewAI Studio sur localhost."""
    ports = ports or [8000, 8080, 3000, 5000]
    for port in ports:
        try:
            resp = requests.get(f"http://localhost:{port}/api/status", timeout=0.5)
            if resp.ok:
                return f"http://localhost:{port}"
        except requests.RequestException:
            pass
    return None

def cli():
    # Charger config OS-spécifique pour les variables d'environnement
    conf_files = ['.local.conf']
    if os.name == 'nt':
        conf_files = ['.windows.conf', '.win.conf'] + conf_files
    for cf in conf_files:
        p = Path(cf)
        if p.is_file():
            for ln in p.read_text().splitlines():
                ln = ln.strip()
                if not ln or ln.startswith('#'):
                    continue
                if '=' in ln:
                    key, val = ln.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())
            break

    parser = argparse.ArgumentParser(prog="squadmanager")
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    subparsers = parser.add_subparsers(dest="command", required=True)

    sp = subparsers.add_parser("create_project", help="Create a new project")
    sp.add_argument("name", help="Project name")

    sp = subparsers.add_parser("create_team", help="Create a new team")
    sp.add_argument("name", help="Team name")

    sp = subparsers.add_parser("add_member", help="Add a member to a project")
    sp.add_argument("project", help="Project name")
    sp.add_argument("member", help="Member name")

    sp = subparsers.add_parser("add_member_to_team", help="Add a member to a team")
    sp.add_argument("team", help="Team name")
    sp.add_argument("member", help="Member name")

    sp = subparsers.add_parser("assign_project_to_team", help="Assign a project to a team")
    sp.add_argument("team", help="Team name")
    sp.add_argument("project", help="Project name")

    sp = subparsers.add_parser("assign_project_to_all_teams", help="Assign a project to all teams")
    sp.add_argument("project", help="Project name")

    sp = subparsers.add_parser("set_cdc", help="Set CDC for project")
    sp.add_argument("project", help="Project name")
    sp.add_argument("cdc", help="CDC content")

    sp = subparsers.add_parser("get_cdc", help="Get CDC of project")
    sp.add_argument("project", help="Project name")

    sp = subparsers.add_parser("transmit_cdc", help="Transmit CDC of project")
    sp.add_argument("project", help="Project name")

    # Outils divers (mémoire)
    tools_sp = subparsers.add_parser("tools", help="Gestion des outils divers")
    tools_sub = tools_sp.add_subparsers(dest="tools_cmd", required=True)
    tools_sub.add_parser("memory-show", help="Afficher l'historique de la mémoire")
    mstats = tools_sub.add_parser("memory-stats", help="Afficher les statistiques de la mémoire")
    mstats.add_argument("--ttl-days", type=int, help="TTL en jours")
    mstats.add_argument("--max-events", type=int, help="Nombre max d'événements à conserver")
    apply_p = tools_sub.add_parser("memory-apply-policy", help="Appliquer la politique de mémoire")
    apply_p.add_argument("--ttl-days", type=int, help="TTL en jours")
    apply_p.add_argument("--max-events", type=int, help="Nombre max d'événements à conserver")
    reset_mem = tools_sub.add_parser("reset-memories", help="Reset CrewAI memory")
    reset_mem.add_argument("--force", action="store_true", help="Confirmer la suppression sans invite")

    # CrewAI crew commands
    sp = subparsers.add_parser("run", help="Kickoff the crew")
    sp.add_argument("--topic", default="AI LLMs", help="Topic")
    sp.add_argument("--current_year", default=str(datetime.now().year), help="Year")
    sp.add_argument("--once", action="store_true", help="Lancer une seule itération puis quitter")

    sp = subparsers.add_parser("train", help="Train the crew")
    sp.add_argument("n_iterations", type=int, help="Number of iterations")
    sp.add_argument("filename", help="Output filename")
    sp.add_argument("--topic", default="AI LLMs", help="Topic")
    sp.add_argument("--current_year", default=str(datetime.now().year), help="Year")

    sp = subparsers.add_parser("replay", help="Replay the crew")
    sp.add_argument("task_id", help="Task ID")

    # CrewAI Studio commands (YAML-based)
    sp = subparsers.add_parser(
        "studio",
        help="Intégration CrewAI Studio",
        description="Intégration CrewAI Studio",
        formatter_class=RawTextHelpFormatter,
        epilog='''Sub-commands:
  list            Lister les crews
  export <id>     Exporter le crew
  import <file>   Importer le crew
  list-agents     Lister les agents
  export-agent <id> Exporter l'agent
  import-agent <file> Importer l'agent
  list-tasks      Lister les tâches
  export-task <id> Exporter la tâche
  import-task <file> Importer la tâche
  delete-crew <id> Supprimer le crew
  delete-agent <id> Supprimer l'agent
  serve          Lancer l'interface locale de CrewAI Studio (Streamlit)
  stop           Arrêter l'interface locale de CrewAI Studio (Streamlit)'''
    )
    sp.add_argument("--status", action="store_true", help="Vérifier la connexion à CrewAI Studio")
    sp.add_argument("--open", action="store_true", help="Ouvrir CrewAI Studio dans le navigateur")
    studio_sp = sp.add_subparsers(
        dest="studio_cmd",
        required=False,
        help="Sub-commands for CrewAI Studio",
        title="studio subcommands",
        description="Sous-commandes disponibles pour CrewAI Studio",
        metavar="COMMAND"
    )
    studio_sp.add_parser("list", help="Lister les crews existants")
    exp = studio_sp.add_parser("export", help="Exporter la config d'un crew depuis Studio")
    exp.add_argument("crew_id", help="ID du crew à exporter")
    exp.add_argument("-o", "--output", help="Fichier YAML de sortie (stdout sinon)", default=None)
    imp = studio_sp.add_parser("import", help="Importer un crew dans Studio depuis YAML")
    imp.add_argument("file", help="Fichier YAML du crew à importer")
    studio_sp.add_parser("list-agents", help="Lister les agents existants")
    exp_a = studio_sp.add_parser("export-agent", help="Exporter la config d'un agent depuis Studio")
    exp_a.add_argument("agent_id", help="ID de l'agent à exporter")
    exp_a.add_argument("-o", "--output", help="Fichier YAML de sortie (stdout sinon)", default=None)
    imp_a = studio_sp.add_parser("import-agent", help="Importer un agent dans Studio depuis YAML")
    imp_a.add_argument("file", help="Fichier YAML de l'agent à importer")
    studio_sp.add_parser("list-tasks", help="Lister les tâches existantes")
    exp_t = studio_sp.add_parser("export-task", help="Exporter la config d'une tâche depuis Studio")
    exp_t.add_argument("task_id", help="ID de la tâche à exporter")
    exp_t.add_argument("-o", "--output", help="Fichier YAML de sortie (stdout sinon)", default=None)
    imp_t = studio_sp.add_parser("import-task", help="Importer une tâche dans Studio depuis YAML")
    imp_t.add_argument("file", help="Fichier YAML de la tâche à importer")
    delete_cr = studio_sp.add_parser("delete-crew", help="Supprimer un crew depuis Studio")
    delete_cr.add_argument("crew_id", help="ID du crew à supprimer")
    delete_ag = studio_sp.add_parser("delete-agent", help="Supprimer un agent depuis Studio")
    delete_ag.add_argument("agent_id", help="ID de l'agent à supprimer")
    studio_sp.add_parser("serve", help="Lancer l'interface locale de CrewAI Studio (Streamlit)")
    studio_sp.add_parser("stop", help="Arrêter l'interface locale de CrewAI Studio (Streamlit)")

    # Plugin commands
    sp = subparsers.add_parser("plugin", help="Gestion des plugins")
    plugin_sp = sp.add_subparsers(dest="plugin_cmd", required=True)
    plugin_sp.add_parser("list", help="Liste des plugins")
    hp = plugin_sp.add_parser("health", help="Status d'un plugin")
    hp.add_argument("--plugin", required=True, help="Nom du plugin")
    sd = plugin_sp.add_parser("send", help="Envoyer un événement à un plugin")
    sd.add_argument("--plugin", required=True, help="Nom du plugin")
    sd.add_argument("--payload", required=True, help="Payload JSON de l'événement")

    # Flow squadmanager via CrewAI Flows
    sp = subparsers.add_parser(
        "flow",
        help="Lancer le flow squadmanager via CrewAI Flows"
    )
    sp.add_argument(
        "--topic",
        default="AI LLMs",
        help="Sujet de la tâche initiale"
    )
    sp.add_argument(
        "--year",
        type=int,
        default=datetime.now().year,
        help="Année courante"
    )

    # Test CrewAI CLI
    sp = subparsers.add_parser(
        "test",
        aliases=["crewai_test"],
        help="Lancer les tests intégrés de CrewAI après vérification des prérequis pytest"
    )
    sp.add_argument(
        "--debug",
        action="store_true",
        help="Activer mode debug pour la vérification de prérequis pytest"
    )
    sp.add_argument(
        "crew_name",
        nargs="?",
        help="Nom du crew à tester via crewai test",
    )

    # KPI management commands
    sp = subparsers.add_parser("define_kpi", help="Define a new KPI")
    sp.add_argument("name", help="KPI name")
    sp.add_argument("description", help="KPI description")

    sp = subparsers.add_parser("increment_kpi", help="Increment a KPI")
    sp.add_argument("name", help="KPI name")
    sp.add_argument("--amount", type=int, default=1, help="Amount to increment")

    sp = subparsers.add_parser("get_kpi", help="Get a KPI value")
    sp.add_argument("name", help="KPI name")

    sp = subparsers.add_parser("list_kpis", help="List all KPIs")

    # Export / Import commands for squadmanager data
    sp = subparsers.add_parser("export", help="Export squadmanager data to JSON")
    sp.add_argument("json_file", nargs="?", help="Output JSON file (defaults to stdout)")

    sp = subparsers.add_parser("import", help="Import squadmanager data from JSON")
    sp.add_argument("json_file", help="Input JSON file")

    args = parser.parse_args()
    team = squadmanager()
    if args.command == "create_project":
        print(team.create_project(args.name))
    elif args.command == "create_team":
        print(team.create_team(args.name))
    elif args.command == "add_member":
        print(",".join(team.add_member(args.project, args.member)))
    elif args.command == "add_member_to_team":
        print(",".join(team.add_member_to_team(args.team, args.member)))
    elif args.command == "assign_project_to_team":
        print(",".join(team.assign_project_to_team(args.team, args.project)))
    elif args.command == "assign_project_to_all_teams":
        print(",".join(team.assign_project_to_all_teams(args.project)))
    elif args.command == "set_cdc":
        print(team.set_cdc(args.project, args.cdc))
    elif args.command == "get_cdc":
        print(team.get_cdc(args.project))
    elif args.command == "transmit_cdc":
        print(team.transmit_cdc(args.project))
    # crew commands
    elif args.command == "run":
        # CLI wrapper : lancer crewai run
        try:
            subprocess.run(["crewai", "run"], check=True)
        except subprocess.CalledProcessError as e:
            sys.exit(e.returncode)
        return
    elif args.command == "train":
        subprocess.run(["crewai", "train", str(args.n_iterations), args.filename], check=True)
    elif args.command == "replay":
        subprocess.run(["crewai", "replay", args.task_id], check=True)
    elif args.command == "tools":
        if args.tools_cmd == "memory-show":
            mgr = MemoryManager()
            for event in mgr.load_history():
                print(json.dumps(event, ensure_ascii=False))
            return
        if args.tools_cmd == "memory-stats":
            mgr = MemoryManager()
            history = mgr.load_history()
            print(f"Événements historiques: {len(history)}")
            conn = sqlite3.connect(mgr.db_path)
            cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r[0] for r in cur.fetchall()]
            if tables:
                print("Tables SQLite:")
                for t in tables:
                    count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                    print(f"  - {t}: {count}")
            else:
                print("Aucune table SQLite trouvée")
            conn.close()
            return
        if args.tools_cmd == "memory-apply-policy":
            mgr = MemoryManager()
            policy = MemoryPolicy(ttl_days=args.ttl_days, max_events=args.max_events)
            kept = policy.apply(mgr)
            print(f"Événements conservés suite à la politique: {len(kept)}")
            return
        if args.tools_cmd == "reset-memories":
            if not args.force:
                answer = input("Attention : toutes les mémoires vont être supprimées. Confirmez (o/N) : ")
                if answer.lower() not in ("o","oui","y","yes"):
                    print("Abandon de la réinitialisation des mémoires.")
                    sys.exit(0)
            try:
                subprocess.run(["crewai", "reset-memories"], check=True)
            except subprocess.CalledProcessError as e:
                sys.exit(e.returncode)
            return
    elif args.command == "studio":
        # fallback import only on first run sans sous-commande/status/open
        if args.studio_cmd is None and not args.status and not args.open:
            init_file = Path.home() / '.squadmanager_initialized'
            if not init_file.exists():
                env_url = os.getenv('CREWAI_STUDIO_URL')
                detected_url = auto_detect_studio_url()
                # Lancer le studio local si aucun studio existant
                if not detected_url and not env_url:
                    studio_dir = Path('D:/Scripts/CrewAI-Studio/app')
                    print('Aucun studio local détecté, lancement d\'une instance...')
                    proc = subprocess.Popen(['streamlit','run','app.py','--server.port','8000'], cwd=str(studio_dir))
                    for _ in range(10):
                        time.sleep(1)
                        detected_url = auto_detect_studio_url()
                        if detected_url:
                            break
                    if detected_url:
                        print(f'Studio local démarré sur {detected_url}')
                    else:
                        print('Erreur: impossible de démarrer le studio local')
                target_url = env_url or detected_url or 'https://studio.crewai.com'
                from squadmanager.plugins.studio_plugin import StudioPlugin
                crew_cfg = yaml.safe_load(Path('squadmanagerAI.yml').read_text(encoding='utf-8'))
                StudioPlugin({'url': target_url}).import_crew(crew_cfg)
                print(f'Crew "squadmanagerAI" importé automatiquement sur {target_url}')
                init_file.write_text(datetime.now().isoformat())
        # Utilisation de StudioPlugin
        env_url = os.getenv("CREWAI_STUDIO_URL")
        url = env_url if env_url else auto_detect_studio_url()
        if not url:
            url = "https://studio.crewai.com"
        api_key = os.getenv("CREWAI_STUDIO_API_KEY")
        config = {"studio": {"url": url, "api_key": api_key}}
        pm = PluginManager(config)
        plugin = pm.get_plugin("studio")
        if not plugin:
            print("Plugin 'studio' non chargé")
            sys.exit(1)
        if args.status:
            print(json.dumps(plugin.health_check(), ensure_ascii=False))
            sys.exit(0)
        if args.open:
            plugin.open_ui()
            sys.exit(0)
        if args.studio_cmd == "serve":
            # Lancement de l'UI locale via Streamlit
            backend_dir = os.getenv("CREWAI_STUDIO_BACKEND_DIR") or Path("D:/Scripts/CrewAI-Studio/app").as_posix()
            subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"], cwd=backend_dir, check=True)
            sys.exit(0)
        if args.studio_cmd == "stop":
            # Arrêt de l'UI locale via Streamlit
            proc = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, check=True)
            for line in proc.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 5 and parts[1].endswith(':8501') and parts[3] == 'LISTENING':
                    pid = parts[-1]
                    subprocess.run(['taskkill', '/PID', pid, '/F'], check=True)
            print('Streamlit arrêté.')
            sys.exit(0)
        if args.studio_cmd == "list":
            print(yaml.safe_dump(plugin.list_crews(), allow_unicode=True, sort_keys=False))
            return
        if args.studio_cmd == "export":
            crew = plugin.export_crew(args.crew_id)
            out = yaml.safe_dump(crew, allow_unicode=True, sort_keys=False)
            if args.output:
                Path(args.output).write_text(out, encoding="utf-8")
            else:
                print(out)
            return
        if args.studio_cmd == "import":
            crew_conf = yaml.safe_load(Path(args.file).read_text(encoding="utf-8"))
            res = plugin.import_crew(crew_conf)
            print(yaml.safe_dump(res, allow_unicode=True, sort_keys=False))
            return
        if args.studio_cmd == "list-agents":
            print(yaml.safe_dump(plugin.list_agents(), allow_unicode=True, sort_keys=False))
            return
        if args.studio_cmd == "export-agent":
            agent = plugin.export_agent(args.agent_id)
            out = yaml.safe_dump(agent, allow_unicode=True, sort_keys=False)
            if args.output:
                Path(args.output).write_text(out, encoding="utf-8")
            else:
                print(out)
            return
        if args.studio_cmd == "import-agent":
            agent_conf = yaml.safe_load(Path(args.file).read_text(encoding="utf-8"))
            res = plugin.import_agent(agent_conf)
            print(yaml.safe_dump(res, allow_unicode=True, sort_keys=False))
            return
        if args.studio_cmd == "list-tasks":
            print(yaml.safe_dump(plugin.list_tasks(), allow_unicode=True, sort_keys=False))
            return
        if args.studio_cmd == "export-task":
            task = plugin.export_task(args.task_id)
            out = yaml.safe_dump(task, allow_unicode=True, sort_keys=False)
            if args.output:
                Path(args.output).write_text(out, encoding="utf-8")
            else:
                print(out)
            return
        if args.studio_cmd == "import-task":
            task_conf = yaml.safe_load(Path(args.file).read_text(encoding="utf-8"))
            res = plugin.import_task(task_conf)
            print(yaml.safe_dump(res, allow_unicode=True, sort_keys=False))
            return
        if args.studio_cmd == "delete-crew":
            res = plugin.delete_crew(args.crew_id)
            print(yaml.safe_dump(res, allow_unicode=True, sort_keys=False))
            return
        if args.studio_cmd == "delete-agent":
            res = plugin.delete_agent(args.agent_id)
            print(yaml.safe_dump(res, allow_unicode=True, sort_keys=False))
            return
        parser.print_help()
        sys.exit(1)
    elif args.command == "plugin":
        pm = PluginManager()
        if args.plugin_cmd == "list":
            for name in pm.list_plugins():
                print(name)
            return
        if args.plugin_cmd == "health":
            plugin = pm.get_plugin(args.plugin)
            print(json.dumps(plugin.health_check(), ensure_ascii=False))
            return
        if args.plugin_cmd == "send":
            plugin = pm.get_plugin(args.plugin)
            payload = json.loads(args.payload)
            plugin.send_event(payload)
            return
    elif args.command == "flow":
        # Exécuter le flow squadmanager
        state = DreamteamState(topic=args.topic, year=args.year)
        try:
            DreamteamFlow().run_flow(state)
        except Exception:
            sys.exit(1)
        return
    elif args.command in ("test", "crewai_test"):
        # Exécuter pytest et crewai test si alias
        pytest_cmd = ["pytest", "-vv", "-s"] if args.debug else ["pytest", "-v", "--maxfail=1", "-s"]
        try:
            subprocess.run(pytest_cmd, check=True)
        except subprocess.CalledProcessError as e:
            sys.exit(e.returncode)
        if args.command == "crewai_test":
            # Appeler crewai test [crew_name]
            cmd = ["crewai", "test"]
            if args.crew_name:
                cmd.append(args.crew_name)
            try:
                subprocess.run(cmd, check=True)
            except FileNotFoundError:
                sys.exit("Erreur : CrewAI CLI introuvable. Installez-la via `pip install crewai`.")
            except subprocess.CalledProcessError as e:
                sys.exit(e.returncode)
        return
    elif args.command == "define_kpi":
        team.define_kpi(args.name, args.description)
        print(f"KPI {args.name} defined")
    elif args.command == "increment_kpi":
        team.increment_kpi(args.name, args.amount)
        print(team.get_kpi(args.name))
    elif args.command == "get_kpi":
        print(team.get_kpi(args.name))
    elif args.command == "list_kpis":
        kpis = team.get_all_kpis()
        for n, info in kpis.items():
            print(f"{n}: {info['value']} -- {info['description']}")
    elif args.command == "export":
        mgr = squadmanager()
        data = mgr.export_all()
        if args.json_file:
            with open(args.json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    elif args.command == "import":
        mgr = squadmanager()
        with open(args.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        mgr.import_all(data)
        print("Data imported successfully")
        return
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()
