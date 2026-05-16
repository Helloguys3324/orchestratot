"""
Code Executor Skill — Execute Python code snippets.
"""


def execute_python(code: str) -> str:
    """Execute Python code and return output."""
    import io
    import sys
    from contextlib import redirect_stdout, redirect_stderr

    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exec(code, {"__builtins__": __builtins__})
        output = stdout.getvalue()
        errors = stderr.getvalue()
        if errors:
            return f"Output:\n{output}\nErrors:\n{errors}"
        return output or "Code executed successfully (no output)"
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"
