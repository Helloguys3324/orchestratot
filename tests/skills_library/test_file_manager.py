import pytest
from pathlib import Path
from skills_library.file_manager import read_file, write_file, list_directory

def test_write_and_read_file(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    content = "Hello, world!"

    # Test writing
    write_result = write_file(str(test_file), content)
    assert "File written" in write_result
    assert test_file.exists()

    # Test reading
    read_result = read_file(str(test_file))
    assert read_result == content

def test_read_non_existent_file(tmp_path: Path):
    non_existent_file = tmp_path / "non_existent.txt"
    result = read_file(str(non_existent_file))
    assert "Error reading file" in result

def test_write_file_error():
    # Attempting to write to a root or restricted path to force an error
    # This might behave differently depending on the OS or user permissions,
    # but passing an invalid type or an empty string might cause errors in pathlib on some systems,
    # or just passing a root restricted directory.
    # A robust way to cause an error is passing None, but type hints say str.
    # Let's pass a directory path as the file to write to.
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        result = write_file(d, "content")
        assert "Error writing file" in result

def test_list_directory(tmp_path: Path):
    # Create some files and directories
    (tmp_path / "file1.txt").write_text("1")
    (tmp_path / "file2.txt").write_text("2")
    (tmp_path / "dir1").mkdir()

    result = list_directory(str(tmp_path))
    assert "📄 file1.txt" in result
    assert "📄 file2.txt" in result
    assert "📁 dir1" in result

def test_list_empty_directory(tmp_path: Path):
    result = list_directory(str(tmp_path))
    assert result == "Empty directory"

def test_list_directory_error():
    result = list_directory("/non_existent_directory_for_testing_purposes_12345")
    assert "Error" in result
