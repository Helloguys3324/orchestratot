import pytest
from unittest.mock import patch, MagicMock
from backend.agents.manager import AgentManager
from backend.agents.templates import AGENT_TEMPLATES

@pytest.fixture
def agent_manager():
    with patch("backend.base_manager.BaseManager._load_dict", return_value={}):
        manager = AgentManager()
        return manager

def test_save_agents(agent_manager):
    with patch("backend.base_manager.BaseManager._save_dict") as mock_save:
        agent_manager._save()
        mock_save.assert_called_once_with(agent_manager._agents)

def test_create_agent_with_template(agent_manager):
    template_id = list(AGENT_TEMPLATES.keys())[0]
    with patch("backend.agents.manager.AgentManager._save"):
        agent = agent_manager.create_agent({"template": template_id, "name": "Custom Name"})
        assert agent["template"] == template_id
        assert agent["name"] == "Custom Name"

def test_update_agent(agent_manager):
    with patch("backend.agents.manager.AgentManager._save"):
        agent = agent_manager.create_agent({"name": "Initial Name"})

    with patch("backend.agents.manager.AgentManager._save") as mock_save:
        updated_agent = agent_manager.update_agent(agent["id"], {"name": "Updated Name"})
        assert updated_agent is not None
        assert updated_agent["name"] == "Updated Name"
        mock_save.assert_called_once()

def test_update_agent_not_found(agent_manager):
    assert agent_manager.update_agent("nonexistent", {"name": "Test"}) is None

def test_delete_agent(agent_manager):
    with patch("backend.base_manager.BaseManager._delete_item", return_value=True) as mock_delete:
        result = agent_manager.delete_agent("agent_id")
        assert result is True
        mock_delete.assert_called_once_with(agent_manager._agents, "agent_id")

def test_duplicate_agent(agent_manager):
    with patch("backend.agents.manager.AgentManager._save"):
        agent = agent_manager.create_agent({"name": "Original Agent"})

    with patch("backend.agents.manager.AgentManager._save") as mock_save:
        duplicate = agent_manager.duplicate_agent(agent["id"])
        assert duplicate is not None
        assert duplicate["id"] != agent["id"]
        assert duplicate["name"] == "Original Agent (Copy)"
        mock_save.assert_called()

def test_duplicate_agent_not_found(agent_manager):
    assert agent_manager.duplicate_agent("nonexistent") is None

def test_list_and_get_agent(agent_manager):
    with patch("backend.agents.manager.AgentManager._save"):
        agent1 = agent_manager.create_agent({"name": "Agent 1"})
        agent2 = agent_manager.create_agent({"name": "Agent 2"})

    agents = agent_manager.list_agents()
    assert len(agents) == 2

    retrieved = agent_manager.get_agent(agent1["id"])
    assert retrieved is not None
    assert retrieved["id"] == agent1["id"]
