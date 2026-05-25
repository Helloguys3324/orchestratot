from datetime import datetime, timezone
import abc
import uuid
from pathlib import Path
from backend.config import load_json, save_json

class BaseManager(abc.ABC):
    """Base manager with common file loading/saving logic."""

    def __init__(self, file_path: Path):
        self._file_path = file_path

    @abc.abstractmethod
    def _load(self) -> None:
        pass

    @abc.abstractmethod
    def _save(self) -> None:
        pass

    def _generate_id(self) -> str:
        """Generate an 8-character unique ID."""
        return uuid.uuid4().hex[:8]

    def _get_now_iso(self) -> str:
        """Get current UTC time in ISO format."""
        return datetime.now(timezone.utc).isoformat()

    def _load_dict(self) -> dict:
        """Helper to load a list of items and convert to a dictionary by ID."""
        items_list = load_json(self._file_path, [])
        return {item["id"]: item for item in items_list if "id" in item}

    def _save_dict(self, data_dict: dict) -> None:
        """Helper to save a dictionary of items as a list."""
        save_json(self._file_path, list(data_dict.values()))

    def _delete_item(self, data_dict: dict, item_id: str) -> bool:
        """Delete an item from a dictionary and save."""
        if data_dict.pop(item_id, None):
            self._save()
            return True
        return False
