"""
File Manager Skill — Read and write files.
"""
from pathlib import Path


def read_file(filepath: str) -> str:
    """Read and return file contents."""
    try:
        return Path(filepath).read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(filepath: str, content: str) -> str:
    """Write content to a file."""
    try:
        p = Path(filepath)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"File written: {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def list_directory(dirpath: str) -> str:
    """List contents of a directory."""
    try:
        p = Path(dirpath)
        items = list(p.iterdir())
        result = []
        for item in items:
            prefix = "📁" if item.is_dir() else "📄"
            result.append(f"{prefix} {item.name}")
        return "\n".join(result) if result else "Empty directory"
    except Exception as e:
        return f"Error: {str(e)}"
