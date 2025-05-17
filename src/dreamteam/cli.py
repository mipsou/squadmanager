import argparse
import os
import subprocess
import sys
from datetime import datetime
from dreamteam.core import DreamTeam
from dreamteam.flow import DreamteamFlow, DreamteamState
import json
import sqlite3
from dreamteam.memory import MemoryManager
from dreamteam.memory_policy import MemoryPolicy
from dreamteam.plugin_manager import PluginManager
from importlib.metadata import version as _version, PackageNotFoundError
import requests
import webbrowser

try:
    __version__ = _version('dreamteam')
except PackageNotFoundError:
    __version__ = '0.0.0'

def cli():
    parser = argparse.ArgumentParser(prog="dreamteam")
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

    sp = subparsers.add_parser("reset-memories", help="Reset CrewAI memory")
    sp.add_argument("--force", action="store_true", help="Confirmer la suppression sans invite")

    # Memory CLI commands
    sp = subparsers.add_parser("memory-show", help="Afficher l'historique de la mémoire")
    sp = subparsers.add_parser("memory-stats", help="Afficher les statistiques de la mémoire")
    sp = subparsers.add_parser("memory-apply-policy", help="Appliquer la politique mémoire (TTL, max_events)")
    sp.add_argument("--ttl-days", type=int, help="TTL en jours")
    sp.add_argument("--max-events", type=int, help="Nombre max d'événements à conserver")

    # CrewAI Studio commands
    sp = subparsers.add_parser("studio", help="Gestion de CrewAI Studio")
    sp.add_argument("--status", action="store_true", help="Vérifier la connexion à CrewAI Studio")
    sp.add_argument("--open", action="store_true", help="Ouvrir CrewAI Studio dans le navigateur")

    # Plugin commands
    sp = subparsers.add_parser("plugin", help="Gestion des plugins")
    plugin_sp = sp.add_subparsers(dest="plugin_cmd", required=True)
    plugin_sp.add_parser("list", help="Liste des plugins")
    hp = plugin_sp.add_parser("health", help="Status d'un plugin")
    hp.add_argument("--plugin", required=True, help="Nom du plugin")
    sd = plugin_sp.add_parser("send", help="Envoyer un événement à un plugin")
    sd.add_argument("--plugin", required=True, help="Nom du plugin")
    sd.add_argument("--payload", required=True, help="Payload JSON de l'événement")

    # Flow Dreamteam via CrewAI Flows
    sp = subparsers.add_parser(
        "flow",
        help="Lancer le flow Dreamteam via CrewAI Flows"
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

    args = parser.parse_args()
    team = DreamTeam()
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
    elif args.command == "reset-memories":
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
    elif args.command == "memory-show":
        mgr = MemoryManager()
        for event in mgr.load_history():
            print(json.dumps(event, ensure_ascii=False))
        return
    elif args.command == "memory-stats":
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
    elif args.command == "memory-apply-policy":
        # Applique la politique sur history.jsonl
        # Permet d'utiliser CREWAI_STORAGE_DIR pour tests/env
        mgr = MemoryManager()
        policy = MemoryPolicy(ttl_days=args.ttl_days, max_events=args.max_events)
        kept = policy.apply(mgr)
        print(f"Événements conservés suite à la politique: {len(kept)}")
        return
    elif args.command == "studio":
        # Status or open CrewAI Studio
        url = os.getenv("CREWAI_STUDIO_URL", "https://studio.crewai.com")
        headers = {}
        token = os.getenv("CREWAI_STUDIO_API_KEY")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if args.status:
            resp = requests.get(f"{url}/api/status", headers=headers)
            print(json.dumps(resp.json(), ensure_ascii=False))
            sys.exit(0)
        if args.open:
            webbrowser.open(url)
            sys.exit(0)
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
        if args.command and args.plugin_cmd == "send":
            plugin = pm.get_plugin(args.plugin)
            payload = json.loads(args.payload)
            plugin.send_event(payload)
            return
    elif args.command == "flow":
        # Exécuter le flow Dreamteam
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
            try:
                subprocess.run(["crewai", "test"], check=True)
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
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()
