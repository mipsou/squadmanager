import pytest
from squadmanager.core import squadmanager


def test_create_project():
    team = squadmanager()
    result = team.create_project("test")
    assert result == "Project test created"

def test_add_member():
    team = squadmanager()
    team.create_project("alpha")
    members = team.add_member("alpha", "Alice")
    assert "Alice" in members

def test_set_and_get_cdc():
    team = squadmanager()
    team.create_project("alpha")
    res = team.set_cdc("alpha", "cdctext")
    assert res == "CDC set for project alpha"
    assert team.get_cdc("alpha") == "cdctext"

def test_transmit_cdc():
    team = squadmanager()
    team.create_project("alpha")
    team.set_cdc("alpha", "content")
    assert team.transmit_cdc("alpha") == "content"

def test_create_team():
    team = squadmanager()
    result = team.create_team("team1")
    assert result == "Team team1 created"

def test_add_member_to_team():
    team = squadmanager()
    team.create_team("team1")
    members = team.add_member_to_team("team1", "Bob")
    assert "Bob" in members

def test_assign_project_to_team():
    team = squadmanager()
    team.create_project("proj1")
    team.create_team("team1")
    assigned = team.assign_project_to_team("team1", "proj1")
    assert "proj1" in assigned

def test_assign_project_to_all_teams():
    team = squadmanager()
    team.create_project("globalproj")
    team.create_team("teamA")
    team.create_team("teamB")
    assigned = team.assign_project_to_all_teams("globalproj")
    assert set(assigned) == {"teamA", "teamB"}

def test_send_and_get_messages():
    team = squadmanager()
    team.create_team("team1")
    result = team.send_message("team1", "Hello")
    assert result == "Message sent to team1"
    assert team.get_messages("team1") == ["Hello"]

def test_broadcast_message():
    team = squadmanager()
    team.create_team("team1")
    team.create_team("team2")
    msgs = team.broadcast_message("Broadcast")
    assert msgs == {"team1": ["Broadcast"], "team2": ["Broadcast"]}

def test_define_and_get_kpi():
    team = squadmanager()
    team.define_kpi("projects_created", "Number of projects created")
    # KPI should start at 0
    assert team.get_kpi("projects_created") == 0
    team.increment_kpi("projects_created")
    assert team.get_kpi("projects_created") == 1
    # Defining an existing KPI raises
    with pytest.raises(ValueError):
        team.define_kpi("projects_created", "Duplicate KPI")

def test_increment_undefined_kpi():
    team = squadmanager()
    with pytest.raises(ValueError):
        team.increment_kpi("undefined_kpi")

def test_get_all_kpis():
    team = squadmanager()
    team.define_kpi("tasks_completed", "Tasks completed")
    team.increment_kpi("tasks_completed", 3)
    kpis = team.get_all_kpis()
    assert "tasks_completed" in kpis
    assert kpis["tasks_completed"]["value"] == 3
    assert kpis["tasks_completed"]["description"] == "Tasks completed"

def test_bulk_define_kpis():
    team = squadmanager()
    definitions = {"a": "desc a", "b": "desc b"}
    team.bulk_define_kpis(definitions)
    # KPIs defined and initialized to 0
    assert team.get_kpi("a") == 0
    assert team.get_kpi("b") == 0
    kpis = team.get_all_kpis()
    assert set(kpis.keys()) == {"a", "b"}

def test_report_kpis():
    team = squadmanager()
    defs = {"x": "desc x", "y": "desc y"}
    team.bulk_define_kpis(defs)
    team.increment_kpi("x", 1)
    team.increment_kpi("y", 2)
    report = team.report_kpis()
    assert "x: 1 (desc x)" in report
    assert "y: 2 (desc y)" in report
