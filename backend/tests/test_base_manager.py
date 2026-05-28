import pytest
from pathlib import Path
from backend.base_manager import BaseManager
import json

class DummyManager(BaseManager):
    def _load(self):
        pass
    def _save(self):
        pass

def test_delete_item_empty_dict():
    manager = DummyManager(Path("dummy.json"))
    data = {"item1": {}}
    result = manager._delete_item(data, "item1")
    assert result is True

def test_delete_list_item_empty_dict():
    manager = DummyManager(Path("dummy.json"))
    data = [{"id": "item1"}]
    result = manager._delete_list_item(data, "item1")
    assert result is True

def test_get_now_iso():
    manager = DummyManager(Path("dummy.json"))
    iso = manager._get_now_iso()
    assert isinstance(iso, str)
    assert "T" in iso

def test_save_list(tmp_path):
    file_path = tmp_path / "dummy.json"
    manager = DummyManager(file_path)
    manager._save_list([{"id": "1"}])
    assert json.loads(file_path.read_text()) == [{"id": "1"}]

def test_save_dict(tmp_path):
    file_path = tmp_path / "dummy.json"
    manager = DummyManager(file_path)
    manager._save_dict({"1": {"id": "1"}})
    assert json.loads(file_path.read_text()) == [{"id": "1"}]
