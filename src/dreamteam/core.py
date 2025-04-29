"""
Core module for DreamTeam
"""

import os
TEAMS_DIR = r"D:\Scripts\Teeams"

class DreamTeam:
    def __init__(self):
        self.projects = {}
        self.teams = {}
        self.team_projects = {}

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
