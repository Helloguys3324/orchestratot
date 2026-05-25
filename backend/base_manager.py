import abc
import uuid
from pathlib import Path

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
