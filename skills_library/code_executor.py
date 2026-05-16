"""
Code Executor Skill — Execute Python code snippets.
"""


import ast

def execute_python(code: str) -> str:
    """Execute Python code and return output."""
    import io
    import sys
    from contextlib import redirect_stdout, redirect_stderr

    # Static analysis for basic sandboxing
    forbidden_modules = {"os", "sys", "subprocess", "shutil", "pathlib", "pty", "socket"}
    forbidden_functions = {"open", "exec", "eval", "__import__", "compile", "globals", "locals"}

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"Error: Syntax error: {str(e)}"
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] in forbidden_modules:
                    return f"Error: Execution blocked. Import of module '{alias.name}' is not allowed."
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split('.')[0] in forbidden_modules:
                return f"Error: Execution blocked. Import from module '{node.module}' is not allowed."
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in forbidden_functions:
                    return f"Error: Execution blocked. Function '{node.func.id}' is not allowed."

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
