"""Define the base service class."""
from aws_lambda_powertools.utilities import parameters


class IService:
    """Define the base service class."""

    def __init__(self, api_key_secret_name: str) -> None:
        """Initialize the service."""
        self._api_key_secret_name = api_key_secret_name

    def get_api_key(secret_name: str) -> str:
        """Get a secret from AWS Secrets Manager."""
        secret = parameters.get_secret(secret_name)
        assert isinstance(secret, str), f"Expected string, got {type(secret)}"
        return secret
