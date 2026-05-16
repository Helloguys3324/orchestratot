from backend.agents.manager import AgentManager
from backend.skills.manager import SkillsManager
from backend.sessions.manager import SessionManager
from backend.websocket.handler import ConnectionManager

agent_manager = AgentManager()
skills_manager = SkillsManager()
session_manager = SessionManager(agent_manager)
ws_manager = ConnectionManager()
