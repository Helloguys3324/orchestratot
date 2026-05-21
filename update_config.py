with open("backend/config.py", "r") as f:
    content = f.read()

import re

new_validator = """    @field_validator('default_model', 'router_model', 'base_url', mode='before')
    def validate_empty_strings(cls, v, info):
        if v == "" or (isinstance(v, str) and not v.strip()):
            field_info = cls.model_fields[info.field_name]
            if field_info.default_factory is not None:
                return field_info.default_factory()
            elif getattr(field_info, 'get_default', None) and field_info.get_default() is not None and field_info.get_default() is not PydanticUndefined:
                return field_info.get_default()
        return v

    @field_validator('base_url', mode='before')"""

content = content.replace("    @field_validator('base_url', mode='before')", new_validator)

# Update the json_schema_extra for these fields
content = content.replace('default_model: str = "gemini-2.5-flash"', 'default_model: str = Field(default="gemini-2.5-flash", json_schema_extra={"env_ignore_empty": False})')
content = content.replace('router_model: str = "gemini-3-flash-live"', 'router_model: str = Field(default="gemini-3-flash-live", json_schema_extra={"env_ignore_empty": False})')
content = content.replace('base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"', 'base_url: str = Field(default="https://generativelanguage.googleapis.com/v1beta/openai/", json_schema_extra={"env_ignore_empty": False})')


with open("backend/config.py", "w") as f:
    f.write(content)
