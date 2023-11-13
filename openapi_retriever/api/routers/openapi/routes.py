"""Define the routes for the OpenAPI router."""
from fastapi import Request
from fastapi import APIRouter
from openapi_retriever.api.routers.openapi.models import (
    OpenAPISchemaSearchRequest,
    OpenAPIMetadataSearchResponse,
)
from openapi_retriever.api.services.postman import Postman
from openapi_retriever.api.settings import (
    RUNTIME_SETTINGS_ATTRIBUTE_NAME,
    Settings,
)


ROUTER = APIRouter()


@ROUTER.post("/search", response_model=OpenAPIMetadataSearchResponse)
def search_openapi_schemas(
    search_request: OpenAPISchemaSearchRequest,
    request: Request,
) -> OpenAPIMetadataSearchResponse:
    """Search for OpenAPI schemas."""
    settings: Settings = getattr(request.app.state, RUNTIME_SETTINGS_ATTRIBUTE_NAME)
    postman_client = Postman(settings=settings)
    response = postman_client.search_openapi_schemas(search_request)
    return OpenAPIMetadataSearchResponse(
        search_term=search_request.search_term,
        ranked_schema_metadata=response,
    )
