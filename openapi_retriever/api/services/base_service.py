"""Define the base service class."""
from typing import Union
from aws_lambda_powertools.utilities import parameters
from openapi_retriever.api.services.shared import Cache
from openapi_retriever.api.settings import Settings


class IService:
    """Define the base service class."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the service."""
        self.settings = settings

    @staticmethod
    def retrieve_secret(secret_name: str) -> Union[str, dict, bytes]:
        """Define the method to retrieve a secret."""
        secret = Cache.get(f"secret/{secret_name}")
        if secret:
            return secret
        return parameters.get_secret(secret_name)

    @staticmethod
    def get_api_key(secret_name: str) -> str:
        """Get a secret from AWS Secrets Manager."""
        secret = IService.retrieve_secret(secret_name)
        assert isinstance(secret, str), f"Expected string, got {type(secret)}"
        Cache.set(f"secret/{secret_name}", secret)
        return secret
