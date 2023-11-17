"""Define the routes for the OpenAPI router."""
from fastapi import APIRouter, File, Path, Request, UploadFile
from openapi_retriever.api.routers.openapi.models import (
    OpenAPISchemaSearchRequest,
    OpenAPIMetadataSearchResponse,
    OpenAPISchemaResponse,
)
from openapi_retriever.api.services.postman import Postman
from openapi_retriever.api.services.schema_bucket import SchemaBucket
from openapi_retriever.api.settings import (
    RUNTIME_SETTINGS_ATTRIBUTE_NAME,
    Settings,
)


ROUTER = APIRouter()


@ROUTER.post(
    "/search",
    name="Search for OpenAPI Schemas",
    operation_id="search_openapi_schemas",
    description="Search for OpenAPI schemas in the public Postman Collections repositories.",
    response_model=OpenAPIMetadataSearchResponse,
)
def search_openapi_schemas(
    search_request: OpenAPISchemaSearchRequest,
    request: Request,
) -> OpenAPIMetadataSearchResponse:
    """Search for OpenAPI schemas."""
    settings: Settings = getattr(request.app.state, RUNTIME_SETTINGS_ATTRIBUTE_NAME)
    postman_client = Postman(settings=settings)
    response = postman_client.search_openapi_schemas(search_request)
    return OpenAPIMetadataSearchResponse(
        search_query=search_request.search_query,
        ranked_schema_metadata=response,
    )


@ROUTER.get(
    "/{schema_id}",
    name="Get OpenAPI Schema",
    operation_id="get_openapi_schema",
    description="Retrieve an OpenAPI schema from an id returned from the search endpoint.",
    response_model=OpenAPISchemaResponse
)
def get_openapi_schema(
    request: Request,
    schema_id: str = Path(..., title="The ID of the schema to retrieve."),
) -> OpenAPISchemaResponse:
    """Retrieve an OpenAPI schema."""
    settings: Settings = getattr(request.app.state, RUNTIME_SETTINGS_ATTRIBUTE_NAME)
    postman_client = Postman(settings=settings)
    schema = postman_client.get_openapi_schema(schema_id)
    schema = postman_client.remove_responses_from_openapi(schema)
    return OpenAPISchemaResponse(
        schema_id=schema_id,
        openapi_schema=schema,
    )


@ROUTER.post(
    "/upload-file",
    name="Upload file to S3 and get URL",
    operation_id="upload_file_to_s3_and_get_url",
    description="Uploads a file to an S3 bucket and returns the URL to the file."
)
async def upload_file_to_s3_and_get_url(
    request: Request,
    file: UploadFile = File(..., description="The file to upload.")
) -> dict:
    """Upload file to S3 bucket and return the URL of the file."""
    settings: Settings = getattr(request.app.state, RUNTIME_SETTINGS_ATTRIBUTE_NAME)
    schema_bucket_service = SchemaBucket(settings=settings)
    
    try:
        file_url = schema_bucket_service.upload_file(file=file)
        return {"file_url": file_url}
    except Exception as error:  # pylint: disable=broad-except
        return {"error": str(error)}
