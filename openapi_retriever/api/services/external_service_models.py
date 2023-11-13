"""Define external service models."""
from typing import List, Optional
from enum import Enum
from pydantic import Field
from openapi_retriever.api.routers.shared import BaseAPIModel


class PostmanSearchBody(BaseAPIModel):
    """Define the model for the Postman Search Body."""

    query_text: str = Field(
        ...,
        description="The search text for querying Postman."
    )
    size: int = Field(
        default=10,
        description="The number of search results to return."
    )
    merge_entities: bool = Field(
        default=False,
        description="Whether to merge entities in the search results."
    )
    non_nested_requests: bool = Field(
        default=True,
        description="Whether the requests are non-nested."
    )
    domain: str = Field(
        default="public",
        description="The domain scope of the search."
    )


class PostmanSearchRequest(BaseAPIModel):
    """Define the model for the Postman Search Request."""

    service: str = Field(
        default="search",
        description="The name of the service."
    )
    method: str = Field(
        default="POST",
        description="The HTTP method to use for the search."
    )
    path: str = Field(
        default="/search-all",
        description="The path to the search API."
    )
    body: PostmanSearchBody = Field(
        ...,
        description="The body of the search request."
    )


class PostmanDocumentType(str, Enum):
    """Define the Postman Document Type."""

    COLLECTION = "collection"


class PostmanAPIDocument(BaseAPIModel):
    """Define the model for the OpenAPI Schema."""

    fork_count: Optional[int] = Field(
        default=None,
        description="The number of times the schema has been forked.",
    )
    watcher_count: Optional[int] = Field(
        default=None,
        description="The number of watchers of the schema (i.e. the number of people who have starred the schema).",
    )
    views: int = Field(
        ...,
        description="The number of times the schema has been viewed by users.",
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


class RankedPostmanAPIResult(BaseAPIModel):
    """Define the model for the OpenAPI Schema."""

    score: float = Field(
        ...,
        description="The score of the schema in the search results.",
    )
    normalized_score: Optional[float] = Field(
        ...,
        description="The normalized score of the schema in the search results.",
    )
    document: PostmanAPIDocument = Field(
        ...,
        description="The Postman API Document.",
    )
