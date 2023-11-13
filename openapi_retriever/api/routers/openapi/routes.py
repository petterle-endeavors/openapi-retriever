"""Define the routes for the OpenAPI router."""
from fastapi import Request
from fastapi import APIRouter
from openapi_retriever.api.routers.openapi.models import (
    OpenAPISchemaSearchRequest,
    OpenAPISchemaSearchResponse,
)
from openapi_retriever.api.services.postman import Postman
from openapi_retriever.api.settings import (
    RUNTIME_SETTINGS_ATTRIBUTE_NAME,
    Settings,
)


ROUTER = APIRouter()


ROUTER.post("/search", response_model=OpenAPISchemaSearchResponse)
def search_openapi_schemas(
    search_request: OpenAPISchemaSearchRequest,
    request: Request,
) -> OpenAPISchemaSearchResponse:
    """Search for OpenAPI schemas."""
    settings: Settings = getattr(request.app.state, RUNTIME_SETTINGS_ATTRIBUTE_NAME)
    postman_client = Postman(secret_name=settings.postman_api_key_secret_name)
    