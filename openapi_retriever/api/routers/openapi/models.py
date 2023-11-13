"""Define the models for the OpenAPI router resources."""
from pydantic import Field
from openapi_retriever.api.routers.shared import BaseAPIModel


class OpenAPISchemaSearchRequest(BaseAPIModel):
    """Define the model for the OpenAPI Schema Search Request."""

    search_term: str = Field(
        ...,
        description="The search term to use to search for OpenAPI schemas.",
    )


class RankedOpenAPIMetadata(BaseAPIModel):
    """Define the model for the OpenAPI Schema."""

    score: float = Field(
        ...,
        description="The score of the schema in the search results.",
    )
    normalized_score: float = Field(
        ...,
        description="The normalized score of the schema in the search results.",
    )
    id: str = Field(
        ...,
        description="The ID of the schema.",
    )
    name: str = Field(
        ...,
        description="The name of the schema.",
    )
    description: str = Field(
        ...,
        description="The summary of the schema.",
    )


class OpenAPIMetadataSearchResponse(OpenAPISchemaSearchRequest):
    """Define the model for the OpenAPI Schema Search Response."""

    schemas: list[RankedOpenAPIMetadata] = Field(
        ...,
        description="The list of ranked OpenAPI schemas.",
    )
