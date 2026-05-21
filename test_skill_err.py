from backend.skills.manager import catch_unexpected
from backend.skills.errors import SkillError, SkillInstallError

def check():
    with catch_unexpected(SkillInstallError, "Oops"):
        raise ValueError("Something bad")

try:
    check()
except Exception as e:
    print(repr(e))
