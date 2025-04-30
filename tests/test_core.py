import pytest
from dreamteam.core import DreamTeam


def test_create_project():
    team = DreamTeam()
    result = team.create_project("test")
    assert result == "Project test created"

def test_add_member():
    team = DreamTeam()
    team.create_project("alpha")
    members = team.add_member("alpha", "Alice")
    assert "Alice" in members

def test_set_and_get_cdc():
    team = DreamTeam()
    team.create_project("alpha")
    res = team.set_cdc("alpha", "cdctext")
    assert res == "CDC set for project alpha"
    assert team.get_cdc("alpha") == "cdctext"

def test_transmit_cdc():
    team = DreamTeam()
    team.create_project("alpha")
    team.set_cdc("alpha", "content")
    assert team.transmit_cdc("alpha") == "content"

def test_create_team():
    team = DreamTeam()
    result = team.create_team("team1")
    assert result == "Team team1 created"

def test_add_member_to_team():
    team = DreamTeam()
    team.create_team("team1")
    members = team.add_member_to_team("team1", "Bob")
    assert "Bob" in members

def test_assign_project_to_team():
    team = DreamTeam()
    team.create_project("proj1")
    team.create_team("team1")
    assigned = team.assign_project_to_team("team1", "proj1")
    assert "proj1" in assigned

def test_assign_project_to_all_teams():
    team = DreamTeam()
    team.create_project("globalproj")
    team.create_team("teamA")
    team.create_team("teamB")
    assigned = team.assign_project_to_all_teams("globalproj")
    assert set(assigned) == {"teamA", "teamB"}

def test_send_and_get_messages():
    team = DreamTeam()
    team.create_team("team1")
    result = team.send_message("team1", "Hello")
    assert result == "Message sent to team1"
    assert team.get_messages("team1") == ["Hello"]

def test_broadcast_message():
    team = DreamTeam()
    team.create_team("team1")
    team.create_team("team2")
    msgs = team.broadcast_message("Broadcast")
    assert msgs == {"team1": ["Broadcast"], "team2": ["Broadcast"]}
