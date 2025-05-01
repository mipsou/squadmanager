import argparse
from dreamteam.core import DreamTeam
from dreamteam.crew import Dreamteam as Crew
from datetime import datetime
import subprocess
from pathlib import Path  # Pour gérer le chemin des logs


def cli():
    parser = argparse.ArgumentParser(prog="dreamteam")
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

    sp = subparsers.add_parser("train", help="Train the crew")
    sp.add_argument("n_iterations", type=int, help="Number of iterations")
    sp.add_argument("filename", help="Output filename")
    sp.add_argument("--topic", default="AI LLMs", help="Topic")
    sp.add_argument("--current_year", default=str(datetime.now().year), help="Year")

    sp = subparsers.add_parser("replay", help="Replay the crew")
    sp.add_argument("task_id", help="Task ID")

    sp = subparsers.add_parser("test", help="Test the crew")
    sp.add_argument("n_iterations", type=int, help="Number of iterations")
    sp.add_argument("eval_llm", help="Evaluation LLM")
    sp.add_argument("--topic", default="AI LLMs", help="Topic")
    sp.add_argument("--current_year", default=str(datetime.now().year), help="Year")

    sp = subparsers.add_parser("crewai_test", help="Run crewai CLI tests")

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

    # Removed crewai_test subcommand: use built-in test instead

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
        # Redirection des logs Ollama vers un fichier
        log_path = Path.cwd() / "ollama.log"
        with open(log_path, "w") as log_file:
            subprocess.run(["crewai", "run"], check=True, stdout=log_file, stderr=subprocess.STDOUT)
        # Affichage de la localisation et taille du fichier de log
        size = log_path.stat().st_size
        print(f"Logs Ollama enregistrés dans {log_path} ({size} octet{'s' if size>1 else ''})")
    elif args.command == "train":
        subprocess.run(["crewai", "train", str(args.n_iterations), args.filename], check=True)
    elif args.command == "replay":
        subprocess.run(["crewai", "replay", args.task_id], check=True)
    elif args.command == "test":
        subprocess.run(["crewai", "test", str(args.n_iterations), args.eval_llm], check=True)
    elif args.command == "crewai_test":
        # Comportement officiel : lancer les tests CrewAI sans arguments additionnels
        subprocess.run(["crewai", "test"], check=True)
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
