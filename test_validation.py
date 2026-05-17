from backend.config import ConfigModel
from pydantic import ValidationError

try:
    # Try validating data explicitly
    model = ConfigModel.model_validate({"api_key": "somekey", "temperature": 0.8})
    print(model.model_dump())

    # Try an invalid save
    ConfigModel.model_validate({"api_key": "somekey", "temperature": "not_a_float"})
except ValidationError as e:
    print("Caught validation error:")
    print(e)
