"""Define service wrapper."""
import json
from typing import Any, Dict
import requests

from openapi_retriever.api.services.base_service import IService
from openapi_retriever.api.routers.openapi.models import (
    RankedOpenAPIMetadata,
    OpenAPISchemaSearchRequest,
    OpenAPISchemaResponse,
)
from openapi_retriever.api.services.external_service_models import (
    PostmanSearchRequest,
    PostmanSearchBody,
    RankedPostmanAPIResult,
)
from openapi_retriever.api.settings import Settings


class Postman(IService):
    """Define the Postman service."""

    def __init__(self,settings: Settings,) -> None:
        """Initialize the service."""
        super().__init__(settings=settings)
        self.api_key = self.get_api_key(secret_name=settings.postman_api_key_secret_name)

    def _ranked_postman_document_to_openapi_metadata(self, doc: RankedPostmanAPIResult) -> RankedOpenAPIMetadata:
        """Convert a Postman document to OpenAPI metadata."""
        return RankedOpenAPIMetadata(
            score=doc.score,
            normalized_score=doc.normalized_score,
            id=doc.document.id,
            name=doc.document.name,
            categories=doc.document.categories,
            fork_count=doc.document.fork_count,
            watcher_count=doc.document.watcher_count,
            num_requests_in_collection=doc.document.num_requests_in_collection,
            views=doc.document.views,
        )

    def search_openapi_schemas(
        self,
        request: OpenAPISchemaSearchRequest,
    ) -> list[RankedOpenAPIMetadata]:
        """Search for OpenAPI schemas."""
        request_body_model = PostmanSearchRequest(
            body=PostmanSearchBody(query_text=request.search_query)
        )
        response = requests.post(
            "https://www.postman.com/_api/ws/proxy",
            headers={
                "Content-Type": "application/json",
                "Host": "www.postman.com",
            },
            data=request_body_model.model_dump_json(by_alias=True),
            timeout=20,
        )
        raw_colletions = response.json()["data"]["collection"]
        validated_collections: list[RankedPostmanAPIResult] = []
        for collection in raw_colletions:
            try:
                validated_collections.append(RankedPostmanAPIResult.model_validate(collection))
            except ValueError:  # pylint: disable=broad-except
                pass
        return [self._ranked_postman_document_to_openapi_metadata(doc) for doc in validated_collections]

    def get_openapi_schema(self, schema_id: str) -> dict:
        """Get an OpenAPI schema."""
        response = requests.get(
            f"https://api.getpostman.com/collections/{schema_id}/transformations",
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
            },
            timeout=20,
        )
        raw_schema = response.json()["output"]
        return json.loads(raw_schema)

    @staticmethod
    def remove_responses_from_openapi(openapi_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove 'responses' keys from all methods within the 'paths' of an OpenAPI schema.

        Parameters
        ----------
        openapi_schema : Dict[str, Any]
            The OpenAPI schema to be modified.

        Returns
        -------
        Dict[str, Any]
            The OpenAPI schema with 'responses' removed from each path's methods.

        Examples
        --------
        >>> dummy_openapi_schema = {
            "openapi": "3.0.0",
            "info": {
                "title": "Sample API",
                "version": "0.1.9"
            },
            "paths": {
                "/pets": {
                    "get": {
                        "summary": "List all pets",
                        "responses": {
                            "200": {
                                "description": "A paged array of pets"
                            }
                        }
                    },
                    "post": {
                        "summary": "Create a pet",
                        "responses": {
                            "201": {
                                "description": "Null response"
                            }
                        }
                    }
                }
            }
        }
        >>> remove_responses_from_openapi(dummy_openapi_schema)
        The returned schema will have the 'responses' keys removed.
        """
        # Check if the 'paths' field exists in the OpenAPI schema to avoid KeyError
        if 'paths' in openapi_schema:
            # Iterate through all paths and methods
            for methods in openapi_schema['paths'].values():
                for method in methods:
                    # Remove 'responses' key if it exists in the method
                    methods[method].pop('responses', None)

        return openapi_schema
