"""Define service wrapper."""
from uuid import uuid4
import json
import boto3
from fastapi import UploadFile
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

    def upload_file(self, file: UploadFile) -> str:
        """
        Upload a file to the bucket and return the URL to the file.
        
        :param file: UploadFile object received from a client.
        :return: The URL of the uploaded file.
        """
        s3_client = boto3.client("s3")

        file_extension = file.filename.split(".")[-1]
        key = f"{uuid4().hex}.{file_extension}"
        
        try:
            s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                key,
                ExtraArgs={
                    "ContentType": file.content_type,
                    "ContentDisposition": f"attachment; filename={file.filename}"
                }
            )
        except Exception as e:
            raise Exception(f"Failed to upload file to S3: {str(e)}")  # pylint: disable=raise-missing-from, broad-exception-raised
        
        return f"https://{self.bucket_name}.s3.amazonaws.com/{key}"
