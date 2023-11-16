"""Define service wrapper."""
from uuid import uuid4
import json
import boto3
from openapi_retriever.api.services.base_service import IService
from openapi_retriever.api.settings import Settings


class SchemaBucket(IService):
    """Define the Postman service."""

    def __init__(self,settings: Settings,) -> None:
        """Initialize the service."""
        super().__init__(settings=settings)
        self.bucket_name = settings.schema_bucket_name

    def _put(self, schema: dict) -> str:
        """Put the schema in the bucket."""
        bucket = boto3.resource("s3").Bucket(self.bucket_name)
        object = bucket.put_object(
            Key=uuid4().hex + ".json",
            Body=json.dumps(schema),
        )
        return f"https://{self.bucket_name}.s3.amazonaws.com/{object.key}"

    def put(self, schema: dict) -> str:
        """Put the schema in the bucket."""
        return self._put(schema=schema)
