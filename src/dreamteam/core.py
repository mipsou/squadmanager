"""
Core module for DreamTeam
"""

import os
# Directory where teams are stored (corrected folder name)
TEAMS_DIR = r"D:\Scripts\Teams"

class DreamTeam:
    def __init__(self):
        self.projects = {}
        self.teams = {}
        self.team_projects = {}
        # Message storage for team communications
        self.messages = {}
        # KPI storage for tracking metrics
        self.kpis = {}

    def create_project(self, name: str) -> str:
        """
        Create a new project with the given name.
        """
        self.projects[name] = {"members": [], "cdc": None}
        return f"Project {name} created"

    def add_member(self, project: str, member: str) -> list:
        """
        Add a member to the specified project.
        """
        if project not in self.projects:
            raise ValueError(f"Project {project} does not exist")
        self.projects[project]["members"].append(member)
        return self.projects[project]["members"]

    def set_cdc(self, project: str, cdc: str) -> str:
        """
        Set CDC for the specified project.
        """
        if project not in self.projects:
            raise ValueError(f"Project {project} does not exist")
        self.projects[project]["cdc"] = cdc
        return f"CDC set for project {project}"

    def get_cdc(self, project: str) -> str:
        """
        Get CDC for the specified project.
        """
        if project not in self.projects:
            raise ValueError(f"Project {project} does not exist")
        return self.projects[project]["cdc"]

    def transmit_cdc(self, project: str) -> str:
        """
        Transmit CDC for the specified project.
        """
        return self.get_cdc(project)

    def create_team(self, name: str) -> str:
        """
        Create a new team with the given name.
        """
        # create directory for the team
        os.makedirs(os.path.join(TEAMS_DIR, name), exist_ok=True)
        self.teams[name] = []
        return f"Team {name} created"

    def add_member_to_team(self, team: str, member: str) -> list:
        """
        Add a member to the specified team.
        """
        if team not in self.teams:
            raise ValueError(f"Team {team} does not exist")
        self.teams[team].append(member)
        return self.teams[team]

    def assign_project_to_team(self, team: str, project: str) -> list:
        """
        Assign a project to a team.
        """
        if team not in self.teams:
            raise ValueError(f"Team {team} does not exist")
        if project not in self.projects:
            raise ValueError(f"Project {project} does not exist")
        self.team_projects.setdefault(team, []).append(project)
        return self.team_projects[team]

    def assign_project_to_all_teams(self, project: str) -> list:
        """
        Assign a project to all existing teams.
        """
        if project not in self.projects:
            raise ValueError(f"Project {project} does not exist")
        assigned = []
        for team in self.teams:
            self.team_projects.setdefault(team, []).append(project)
            assigned.append(team)
        return assigned

    def send_message(self, team: str, message: str) -> str:
        """Send a message from a team to DreamTeam."""
        if team not in self.teams:
            raise ValueError(f"Team {team} does not exist")
        self.messages.setdefault(team, []).append(message)
        return f"Message sent to {team}"

    def get_messages(self, team: str) -> list:
        """Retrieve messages sent by a team."""
        if team not in self.teams:
            raise ValueError(f"Team {team} does not exist")
        return self.messages.get(team, [])

    def broadcast_message(self, message: str) -> dict:
        """Broadcast a message to all teams."""
        for tm in self.teams:
            self.messages.setdefault(tm, []).append(message)
        return self.messages

    def define_kpi(self, name: str, description: str) -> None:
        """Define a new KPI with a description."""
        if name in self.kpis:
            raise ValueError(f"KPI {name} already defined")
        self.kpis[name] = {"description": description, "value": 0}

    def bulk_define_kpis(self, definitions: dict) -> None:
        """Define multiple KPIs at once."""
        for name, desc in definitions.items():
            self.define_kpi(name, desc)

    def increment_kpi(self, name: str, amount: int = 1) -> None:
        """Increment an existing KPI by amount."""
        if name not in self.kpis:
            raise ValueError(f"KPI {name} is not defined")
        self.kpis[name]["value"] += amount

    def get_kpi(self, name: str) -> int:
        """Get the current value of a KPI."""
        if name not in self.kpis:
            raise ValueError(f"KPI {name} is not defined")
        return self.kpis[name]["value"]

    def get_all_kpis(self) -> dict:
        """Return all defined KPIs with their descriptions and values."""
        return self.kpis

    def report_kpis(self) -> str:
        """Generate a textual report of KPIs."""
        lines = [f"{name}: {info['value']} ({info['description']})" for name, info in self.kpis.items()]
        return "\n".join(lines)
