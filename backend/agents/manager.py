"""
Agent Manager — handles agent CRUD and AutoGen agent creation.
"""
from typing import Optional
from backend.config import AGENTS_FILE
from backend.agents.templates import get_template, AGENT_TEMPLATES
from backend.base_manager import BaseManager



class AgentManager(BaseManager):
    """Manages agent configurations and lifecycle."""

    UPDATABLE_FIELDS = [
        "name", "icon", "color", "description", "system_prompt",
        "skills", "model", "temperature", "max_tokens", "enabled",
    ]

    def __init__(self):
        self._agents: dict[str, dict] = {}
        super().__init__(AGENTS_FILE)
        self._load()

    def _load(self):
        """Load agents from disk."""
        self._agents = self._load_dict()

    def _save(self):
        """Persist agents to disk."""
        self._save_dict(self._agents)

    def list_agents(self) -> list[dict]:
        """List all configured agents."""
        return list(self._agents.values())

    def get_agent(self, agent_id: str) -> Optional[dict]:
        """Get a single agent by ID."""
        return self._agents.get(agent_id)

    def create_agent(self, data: dict) -> dict:
        """Create a new agent from provided data."""
        agent_id = self._generate_id()

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

        merged = {**defaults, **base, **data}
        agent.update({k: merged[k] for k in self.UPDATABLE_FIELDS if k in merged})

        self._agents[agent_id] = agent
        self._save()
        return agent

    def update_agent(self, agent_id: str, data: dict) -> Optional[dict]:
        """Update an existing agent."""
        if agent := self._agents.get(agent_id):
            # Update only provided fields
            agent.update({k: data[k] for k in self.UPDATABLE_FIELDS if k in data})
            self._agents[agent_id] = agent
            self._save()
            return agent
        return None

    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent."""
        return self._delete_item(self._agents, agent_id)

    def duplicate_agent(self, agent_id: str) -> Optional[dict]:
        """Duplicate an existing agent with a new ID."""
        if source := self._agents.get(agent_id):
            source = source.copy()
            source["name"] = f"{source['name']} (Copy)"
            # Remove the old ID so create_agent generates a new one
            del source["id"]
            return self.create_agent(source)
        return None
