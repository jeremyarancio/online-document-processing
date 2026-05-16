from typing import BinaryIO
from io import BytesIO

import boto3

from app.application.ports.storage import IStorageService
from app.domain.document import DocumentId


class S3StorageService(IStorageService):
    def __init__(self, bucket_name: str, region: str) -> None:
        self._bucket_name = bucket_name
        self._client = boto3.client("s3", region_name=region)

    def get_presigned_url(self, document_id: DocumentId) -> str:
        return self._client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self._bucket_name,
                "Key": self._document_key(document_id),
            },
            ExpiresIn=3600,
        )

    def get_document(self, document_id: DocumentId) -> BinaryIO:
        response = self._client.get_object(
            Bucket=self._bucket_name,
            Key=self._document_key(document_id),
        )
        return BytesIO(response["Body"].read())

    def _document_key(self, document_id: DocumentId) -> str:
        return f"documents/{document_id}"
