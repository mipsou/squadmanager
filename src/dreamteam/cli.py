import argparse
from dreamteam.core import DreamTeam
from dreamteam.crew import Dreamteam as Crew
from datetime import datetime


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
        crew = Crew()
        inputs = {"topic": args.topic, "current_year": args.current_year}
        crew.crew().kickoff(inputs=inputs)
    elif args.command == "train":
        crew = Crew()
        inputs = {"topic": args.topic, "current_year": args.current_year}
        crew.crew().train(n_iterations=args.n_iterations, filename=args.filename, inputs=inputs)
    elif args.command == "replay":
        Crew().crew().replay(task_id=args.task_id)
    elif args.command == "test":
        # Execute crewAI test and print result
        crew_instance = Crew()
        inputs = {"topic": args.topic, "current_year": args.current_year}
        result = crew_instance.crew().test(
            n_iterations=args.n_iterations,
            eval_llm=args.eval_llm,
            inputs=inputs
        )
        if result is not None:
            print(result)
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
