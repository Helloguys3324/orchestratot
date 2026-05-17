from backend.config import ConfigModel, get_settings, save_settings
from pydantic import ValidationError

settings = get_settings()
settings.update({"temperature": "invalid_float", "api_key": "valid_key_123!"})

try:
    save_settings(settings)
    print("save_settings allowed invalid config!")
except ValidationError as e:
    print("Caught validation error during save_settings:")
    print(e)
