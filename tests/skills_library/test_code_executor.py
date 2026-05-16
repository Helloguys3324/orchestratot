import pytest
from skills_library.code_executor import execute_python

def test_execute_python_success():
    code = "print('Hello, world!')"
    result = execute_python(code)
    assert "Hello, world!" in result

def test_execute_python_no_output():
    code = "x = 1 + 1"
    result = execute_python(code)
    assert "Code executed successfully" in result

def test_execute_python_blocked_import():
    code = "import os\nprint(os.getcwd())"
    result = execute_python(code)
    assert "Error: Execution blocked" in result
    assert "Import of module 'os' is not allowed" in result

def test_execute_python_blocked_import_from():
    code = "from subprocess import call\ncall(['ls'])"
    result = execute_python(code)
    assert "Error: Execution blocked" in result
    assert "Import from module 'subprocess' is not allowed" in result

def test_execute_python_blocked_function():
    code = "f = open('test.txt', 'w')"
    result = execute_python(code)
    assert "Error: Execution blocked" in result
    assert "Function 'open' is not allowed" in result

def test_execute_python_syntax_error():
    code = "print('Hello"
    result = execute_python(code)
    assert "Error: Syntax error" in result

def test_execute_python_runtime_error():
    code = "print(1 / 0)"
    result = execute_python(code)
    assert "Error: ZeroDivisionError" in result
