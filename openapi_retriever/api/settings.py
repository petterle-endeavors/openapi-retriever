"""Define runtime settings for the API."""
from pydantic_settings import BaseSettings


RUNTIME_SETTINGS_ATTRIBUTE_NAME = "runtime_settings"


class Settings(BaseSettings):
    """Define the settings for the API."""

    postman_api_key_secret_name: str = "postman_api_key"
    schema_bucket_name: str
