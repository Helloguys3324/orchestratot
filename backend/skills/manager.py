"""
Skills Manager — handles skill CRUD, loading, and marketplace.
"""
import importlib.util
import inspect
from functools import wraps
from typing import Callable, Any, TypeVar, ParamSpec
import httpx
from contextlib import contextmanager, asynccontextmanager
from collections.abc import Iterator, AsyncIterator
import json
from pathlib import Path
from backend.config import SKILLS_FILE, SKILLS_DIR, CUSTOM_SKILLS_DIR, load_json, save_json
from backend.skills.errors import SkillError, SkillValidationError, SkillInstallError, SkillNotFoundError
from backend.base_manager import BaseManager


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



def _handle_unexpected_error(e: Exception, error_cls: type[SkillError], msg_prefix: str) -> None:
    if isinstance(e, SkillError):
        raise e
    error_name = type(e).__name__
    raise error_cls(f"{msg_prefix}: {error_name} - {e}") from e

@contextmanager
def catch_unexpected(error_cls: type[SkillError], msg_prefix: str) -> Iterator[None]:
    try:
        yield
    except Exception as e:
        _handle_unexpected_error(e, error_cls, msg_prefix)

@asynccontextmanager
async def async_catch_unexpected(error_cls: type[SkillError], msg_prefix: str) -> AsyncIterator[None]:
    try:
        yield
    except Exception as e:
        _handle_unexpected_error(e, error_cls, msg_prefix)


P = ParamSpec("P")
T = TypeVar("T")

def handle_skill_errors(error_cls: type[SkillError], msg_prefix: str) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
                async with async_catch_unexpected(error_cls, msg_prefix):
                    return await func(*args, **kwargs)
            return async_wrapper # type: ignore
        else:
            @wraps(func)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
                with catch_unexpected(error_cls, msg_prefix):
                    return func(*args, **kwargs)
            return sync_wrapper # type: ignore
    return decorator

class SkillsManager(BaseManager):
    def __init__(self):
        self._custom_skills: list[dict] = []
        super().__init__(SKILLS_FILE)
        self._load()

    def _load(self) -> None:
        with catch_unexpected(SkillError, "Failed to load skills file"):
            self._custom_skills = self._load_list()

    def _save(self) -> None:
        with catch_unexpected(SkillError, "Failed to save skills file"):
            self._save_list(self._custom_skills)

    @handle_skill_errors(SkillError, "Failed to list skills")
    def list_skills(self) -> list[dict]:
        return BUILTIN_SKILLS + self._custom_skills

    @handle_skill_errors(SkillError, "Failed to list marketplace skills")
    def list_marketplace(self) -> list[dict]:
        return MARKETPLACE_SKILLS

    @handle_skill_errors(SkillError, "Failed to get skill")
    def get_skill(self, skill_id: str) -> dict | None:
        if s := next((s for s in BUILTIN_SKILLS + self._custom_skills if s["id"] == skill_id), None):
            return s

        raise SkillNotFoundError("Skill not found")

    def _write_skill_file(self, skill_id: str, code: str) -> str:
        filepath = CUSTOM_SKILLS_DIR / f"{skill_id}.py"
        with catch_unexpected(SkillError, "Failed to write skill file"):
            filepath.write_text(code, encoding="utf-8")
        return f"{skill_id}.py"

    def _validate_string_field(self, data: dict, field: str, default: str = "", required: bool = False) -> str:
        if not isinstance(data, dict):
            raise SkillValidationError("Invalid skill data provided")
        value = data.get(field, default)
        if required and not value:
            raise SkillValidationError(f"Skill {field} is required")
        if not isinstance(value, str):
            raise SkillValidationError(f"Skill {field} must be a string")
        return value

    def _add_custom_skill(self, prefix: str, data: dict, default_category: str, source: str) -> dict:
        with catch_unexpected(SkillValidationError, "Invalid skill data provided"):
            name = self._validate_string_field(data, "name", required=True)
            icon = self._validate_string_field(data, "icon", default="🔧" if prefix == "custom" else "📦")
            description = self._validate_string_field(data, "description", default="")
            category = self._validate_string_field(data, "category", default=default_category)
            skill_code = self._validate_string_field(data, "code", default="")

        skill_id = f"{prefix}_{self._generate_id()}"
        skill = {
            "id": skill_id,
            "name": name,
            "icon": icon,
            "description": description,
            "category": category,
            "builtin": False,
            "enabled": True,
            "source": source,
            "code": skill_code,
        }
        if skill["code"]:
            skill["file"] = self._write_skill_file(skill_id, skill["code"])

        self._custom_skills.append(skill)
        self._save()
        return skill

    @handle_skill_errors(SkillError, "Failed to create skill")
    def create_skill(self, data: dict) -> dict:
        return self._add_custom_skill("custom", data, "custom", "custom")

    @handle_skill_errors(SkillError, "Failed to delete skill")
    def delete_skill(self, skill_id: str) -> bool:
        skill = next((s for s in self._custom_skills if s["id"] == skill_id), None)

        if skill:
            # Remove file if exists
            filepath = CUSTOM_SKILLS_DIR / f"{skill_id}.py"
            with catch_unexpected(SkillError, "Failed to delete skill file"):
                if filepath.exists():
                    filepath.unlink()

            self._delete_list_item(self._custom_skills, skill_id)
            return True

        raise SkillNotFoundError("Skill not found")

    @handle_skill_errors(SkillInstallError, "Failed to install skill")
    async def install_from_url(self, url: str, name: str = None) -> dict:
        """Download and install a skill from a URL."""
        from urllib.parse import urlparse
        if not isinstance(url, str):
            raise SkillValidationError("Invalid URL format: URL must be a string")

        with catch_unexpected(SkillValidationError, "Invalid URL format"):
            parsed_url = urlparse(url)

        if parsed_url.scheme not in ("http", "https"):
            raise SkillValidationError("Invalid URL scheme. Only http and https are allowed.")
        if parsed_url.hostname in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
            raise SkillValidationError("Invalid URL hostname. Localhost is not allowed.")

        async with async_catch_unexpected(SkillInstallError, "Failed to download skill"):
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                resp.raise_for_status()
                code = resp.text

        data = {
            "name": name or "Imported Skill",
            "description": f"Imported from {url}",
            "code": code,
        }
        return self._add_custom_skill("imported", data, "imported", url)
