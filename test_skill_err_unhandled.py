from backend.api.skills import handle_skill_exceptions
try:
    with handle_skill_exceptions():
        raise Exception("Oops")
except Exception as e:
    print("Caught:", repr(e))
