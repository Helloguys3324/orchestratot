class SkillError(Exception):
    """Base exception for skill-related errors."""
    pass

class SkillValidationError(SkillError):
    """Raised when skill data or URL is invalid."""
    pass

class SkillInstallError(SkillError):
    """Raised when installing a skill fails (e.g., download failed)."""
    pass

class SkillNotFoundError(SkillError):
    """Raised when a requested skill is not found."""
    pass
