"""
Agent Manager — handles agent CRUD and AutoGen agent creation.
"""
import uuid
from typing import Optional
from backend.config import AGENTS_FILE, load_json, save_json
from backend.agents.templates import get_template, AGENT_TEMPLATES


class AgentManager:
    """Manages agent configurations and lifecycle."""

    UPDATABLE_FIELDS = [
        "name", "icon", "color", "description", "system_prompt",
        "skills", "model", "temperature", "max_tokens", "enabled",
    ]

    def __init__(self):
        self._agents: dict[str, dict] = {}
        self._load()

    def _load(self):
        """Load agents from disk."""
        agents_list = load_json(AGENTS_FILE, [])
        self._agents = {a["id"]: a for a in agents_list}

    def _save(self):
        """Persist agents to disk."""
        save_json(AGENTS_FILE, list(self._agents.values()))

    def list_agents(self) -> list[dict]:
        """List all configured agents."""
        return list(self._agents.values())

    def get_agent(self, agent_id: str) -> Optional[dict]:
        """Get a single agent by ID."""
        return self._agents.get(agent_id)

    def create_agent(self, data: dict) -> dict:
        """Create a new agent from provided data."""
        agent_id = str(uuid.uuid4())[:8]

        # If a template is specified, use it as base
        template_id = data.get("template")
        if template_id and template_id in AGENT_TEMPLATES:
            template = get_template(template_id)
            base = {
                "name": template["name"],
                "icon": template["icon"],
                "color": template["color"],
                "description": template["description"],
                "system_prompt": template["system_prompt"],
                "skills": template["suggested_skills"],
            }
        else:
            base = {
                "name": "Custom Agent",
                "icon": "🤖",
                "color": "#64748B",
                "description": "",
                "system_prompt": "You are a helpful AI assistant.",
                "skills": [],
            }

        # Defaults specifically mentioned in the original logic
        defaults = {
            "model": "gemini-2.5-flash",
            "temperature": 0.7,
            "max_tokens": 4096,
            "enabled": True,
        }

        # Override with user-provided values
        agent = {
            "id": agent_id,
            "template": template_id or "custom",
        }

        for field in self.UPDATABLE_FIELDS:
            # Fallback priority: data -> base -> defaults
            if field in data:
                agent[field] = data[field]
            elif field in base:
                agent[field] = base[field]
            elif field in defaults:
                agent[field] = defaults[field]

        self._agents[agent_id] = agent
        self._save()
        return agent

    def update_agent(self, agent_id: str, data: dict) -> Optional[dict]:
        """Update an existing agent."""
        if agent_id not in self._agents:
            return None

        agent = self._agents[agent_id]
        # Update only provided fields
        for field in self.UPDATABLE_FIELDS:
            if field in data:
                agent[field] = data[field]

        self._agents[agent_id] = agent
        self._save()
        return agent

    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent."""
        if agent_id in self._agents:
            del self._agents[agent_id]
            self._save()
            return True
        return False

    def duplicate_agent(self, agent_id: str) -> Optional[dict]:
        """Duplicate an existing agent with a new ID."""
        if agent_id not in self._agents:
            return None

        source = self._agents[agent_id].copy()
        source["name"] = f"{source['name']} (Copy)"
        # Remove the old ID so create_agent generates a new one
        del source["id"]
        return self.create_agent(source)
