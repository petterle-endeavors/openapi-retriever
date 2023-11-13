"""Define service wrapper."""
import requests
from openapi_retriever.api.services.base_service import IService
from openapi_retriever.api.routers.openapi.models import (
    RankedOpenAPIMetadata,
    OpenAPISchemaSearchRequest,
)
from openapi_retriever.api.services.external_service_models import (
    PostmanSearchRequest,
    PostmanSearchBody,
    RankedPostmanAPIResult,
)


class Postman(IService):
    """Define the Postman service."""

    def __init__(self, secret_name: str) -> None:
        """Initialize the service."""
        self.api_key = self.get_api_key(secret_name)

    def search_openapi_schemas(
        self,
        request: OpenAPISchemaSearchRequest,
    ) -> list[RankedOpenAPIMetadata]:
        """Search for OpenAPI schemas."""
        # req?uest should have:
        # Content-Length
        # Content-Type
        # Host
        request_body_model = PostmanSearchRequest(
            body=PostmanSearchBody(query_text=request.search_term)
        )
        request_body = request_body_model.model_dump_json()
        response = requests.post(
            "https://api.getpostman.com/collections",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
                "Host": "www.postman.com",
                "Content-Length": str(len(request_body)),
            },
            json=request_body,
            timeout=10,
        )
        raw_colletions = response.json()["data"]["json"]
        validated_collections = []
        for collection in raw_colletions:
            validated_collections.append(RankedPostmanAPIResult.model_validate(collection))
