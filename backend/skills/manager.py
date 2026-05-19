"""
Skills Manager — handles skill CRUD, loading, and marketplace.
"""
import uuid
import importlib.util
import httpx
import json
from pathlib import Path
from backend.config import SKILLS_FILE, SKILLS_DIR, CUSTOM_SKILLS_DIR, load_json, save_json
from backend.skills.errors import SkillValidationError, SkillInstallError, SkillNotFoundError


# Built-in skills metadata
BUILTIN_SKILLS = [
    {
        "id": "code_executor",
        "name": "Code Executor",
        "icon": "▶️",
        "description": "Execute Python code in a sandboxed environment",
        "category": "development",
        "builtin": True,
        "enabled": True,
        "source": "builtin",
        "file": "code_executor.py",
    },
    {
        "id": "web_search",
        "name": "Web Search",
        "icon": "🔍",
        "description": "Search the web for information",
        "category": "research",
        "builtin": True,
        "enabled": True,
        "source": "builtin",
        "file": "web_search.py",
    },
    {
        "id": "file_manager",
        "name": "File Manager",
        "icon": "📁",
        "description": "Read, write, and manage files",
        "category": "utility",
        "builtin": True,
        "enabled": True,
        "source": "builtin",
        "file": "file_manager.py",
    },
    {
        "id": "data_analysis",
        "name": "Data Analysis",
        "icon": "📊",
        "description": "Analyze data with pandas and numpy",
        "category": "analytics",
        "builtin": True,
        "enabled": True,
        "source": "builtin",
        "file": "data_analyst.py",
    },
]

# Marketplace catalog (simulated)
MARKETPLACE_SKILLS = [
    {
        "id": "mp_langchain_tools",
        "name": "LangChain Tools Pack",
        "icon": "🔗",
        "description": "Integration with LangChain tools ecosystem",
        "category": "integration",
        "author": "community",
        "downloads": 1250,
        "url": "https://raw.githubusercontent.com/example/skills/main/langchain_tools.py",
    },
    {
        "id": "mp_api_caller",
        "name": "REST API Caller",
        "icon": "🌐",
        "description": "Make HTTP requests to any REST API",
        "category": "integration",
        "author": "community",
        "downloads": 890,
        "url": "https://raw.githubusercontent.com/example/skills/main/api_caller.py",
    },
    {
        "id": "mp_db_query",
        "name": "Database Query",
        "icon": "🗄️",
        "description": "Query SQL and NoSQL databases",
        "category": "data",
        "author": "community",
        "downloads": 756,
        "url": "https://raw.githubusercontent.com/example/skills/main/db_query.py",
    },
    {
        "id": "mp_image_gen",
        "name": "Image Generator",
        "icon": "🎨",
        "description": "Generate images using AI models",
        "category": "creative",
        "author": "community",
        "downloads": 2100,
        "url": "https://raw.githubusercontent.com/example/skills/main/image_gen.py",
    },
    {
        "id": "mp_email_sender",
        "name": "Email Sender",
        "icon": "📧",
        "description": "Send emails via SMTP",
        "category": "communication",
        "author": "community",
        "downloads": 430,
        "url": "https://raw.githubusercontent.com/example/skills/main/email_sender.py",
    },
]


class SkillsManager:
    def __init__(self):
        self._custom_skills: list[dict] = []
        self._load()

    def _load(self) -> None:
        try:
            self._custom_skills = load_json(SKILLS_FILE, [])
        except (json.JSONDecodeError, OSError) as e:
            raise SkillInstallError(f"Failed to load skills file: {e}") from e

    def _save(self) -> None:
        try:
            save_json(SKILLS_FILE, self._custom_skills)
        except (TypeError, ValueError, OSError) as e:
            raise SkillInstallError(f"Failed to save skills file: {e}") from e

    def list_skills(self) -> list[dict]:
        return BUILTIN_SKILLS + self._custom_skills

    def list_marketplace(self) -> list[dict]:
        return MARKETPLACE_SKILLS

    def get_skill(self, skill_id: str) -> dict | None:
        for s in BUILTIN_SKILLS + self._custom_skills:
            if s["id"] == skill_id:
                return s

        raise SkillNotFoundError("Skill not found")

    def _write_skill_file(self, skill_id: str, code: str) -> str:
        filepath = CUSTOM_SKILLS_DIR / f"{skill_id}.py"
        try:
            filepath.write_text(code, encoding="utf-8")
        except OSError as e:
            raise SkillInstallError(f"Failed to write skill file: {e}") from e
        return f"{skill_id}.py"

    def create_skill(self, data: dict) -> dict:
        try:
            if not data.get("name"):
                raise SkillValidationError("Skill name is required")
        except AttributeError as e:
            raise SkillValidationError("Invalid skill data provided") from e

        skill_code = data.get("code", "")
        if not isinstance(skill_code, str):
            raise SkillValidationError("Skill code must be a string")

        skill_id = f"custom_{uuid.uuid4().hex[:8]}"
        skill = {
            "id": skill_id,
            "name": data.get("name"),
            "icon": data.get("icon", "🔧"),
            "description": data.get("description", ""),
            "category": data.get("category", "custom"),
            "builtin": False,
            "enabled": True,
            "source": "custom",
            "code": skill_code,
        }
        # Save code to file
        if skill["code"]:
            skill["file"] = self._write_skill_file(skill_id, skill["code"])

        self._custom_skills.append(skill)
        self._save()
        return skill

    def delete_skill(self, skill_id: str) -> bool:
        for i, s in enumerate(self._custom_skills):
            if s["id"] == skill_id:
                # Remove file if exists
                filepath = CUSTOM_SKILLS_DIR / f"{skill_id}.py"
                if filepath.exists():
                    try:
                        filepath.unlink()
                    except OSError as e:
                        raise SkillInstallError(f"Failed to delete skill file: {e}") from e
                self._custom_skills.pop(i)
                self._save()
                return True

        raise SkillNotFoundError("Skill not found")

    async def install_from_url(self, url: str, name: str = None) -> dict:
        """Download and install a skill from a URL."""
        from urllib.parse import urlparse
        try:
            parsed_url = urlparse(url)
        except (ValueError, AttributeError, TypeError) as e:
            raise SkillValidationError(f"Invalid URL format: {e}") from e

        if parsed_url.scheme not in ("http", "https"):
            raise SkillValidationError("Invalid URL scheme. Only http and https are allowed.")
        if parsed_url.hostname in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
            raise SkillValidationError("Invalid URL hostname. Localhost is not allowed.")

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                resp.raise_for_status()
                code = resp.text
        except httpx.HTTPStatusError as e:
            raise SkillInstallError(f"HTTP error occurred: {e.response.status_code} {e.response.reason_phrase}") from e
        except httpx.RequestError as e:
            raise SkillInstallError(f"Request error occurred: {str(e)}") from e

        skill_id = f"imported_{uuid.uuid4().hex[:8]}"
        skill = {
            "id": skill_id,
            "name": name or f"Imported Skill",
            "icon": "📦",
            "description": f"Imported from {url}",
            "category": "imported",
            "builtin": False,
            "enabled": True,
            "source": url,
            "code": code,
        }
        skill["file"] = self._write_skill_file(skill_id, code)

        self._custom_skills.append(skill)
        self._save()
        return skill
