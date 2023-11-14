"""Define the models for the OpenAPI router resources."""
from typing import Optional
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
    normalized_score: Optional[float] = Field(
        ...,
        description="The normalized score of the schema in the search results.",
    )
    views: int = Field(
        ...,
        description="The number of times the schema has been viewed by users.",
    )
    fork_count: Optional[int] = Field(
        default=None,
        description="The number of times the schema has been forked.",
    )
    watcher_count: Optional[int] = Field(
        default=None,
        description="The number of watchers of the schema (i.e. the number of people who have starred the schema).",
    )
    num_requests_in_collection: Optional[int] = Field(
        default=None,
        description="The number of requests in the schema.",
    )
    id: str = Field(
        ...,
        description="The ID of the schema.",
    )
    name: str = Field(
        ...,
        description="The name of the schema.",
    )
    categories: list[str] = Field(
        ...,
        description="The categories of that the schema belongs to.",
    )


class OpenAPIMetadataSearchResponse(OpenAPISchemaSearchRequest):
    """Define the model for the OpenAPI Schema Search Response."""

    ranked_schema_metadata: list[RankedOpenAPIMetadata] = Field(
        ...,
        description="The list of ranked OpenAPI schemas.",
    )


class OpenAPISchemaResponse(BaseAPIModel):
    """Define the model for the OpenAPI Schema Response."""

    id: str = Field(
        ...,
        description="The ID of the schema.",
    )
    schema: dict = Field(
        ...,
        description="The OpenAPI schema.",
    )
