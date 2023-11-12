"""Define service wrapper."""
from openapi_retriever.api.services.base_service import IService


class Postman(IService):

    def __init__(self, secret_name: str) -> None:
        """Initialize the service."""
        self._service = None
        self.api_key = self.get_api_key(secret_name)

