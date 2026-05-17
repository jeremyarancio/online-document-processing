from typing import BinaryIO
from uuid import UUID
from io import BytesIO
from pathlib import Path

import boto3

from app.application.ports.storage import IStorageService
from app.domain.document import DocumentId


class S3StorageService(IStorageService):
    def __init__(self, bucket_name: str, region: str, dir: str) -> None:
        self._bucket_name = bucket_name
        self._client = boto3.client("s3", region_name=region)
        self._dir = dir

    def get_presigned_url(self, document_id: DocumentId) -> str:
        return self._client.generate_presigned_url(
            "put_object",
            Params={"Bucket": self._bucket_name, "Key": self._get_path(document_id)},
            ExpiresIn=3600,
        )

    def get_document(self, document_id: DocumentId) -> BinaryIO:
        response = self._client.get_object(
            Bucket=self._bucket_name,
            Key=self._get_path(document_id),
        )
        return BytesIO(response["Body"].read())

    def _get_path(self, id_: UUID) -> str:
        return self._dir + str(id_)


class LocalStorageService(IStorageService):
    def __init__(self, base_dir: Path, dir: str) -> None:
        self._base_dir = base_dir.resolve()
        self._dir = dir

    def get_presigned_url(self, document_id: DocumentId) -> str:
        path = self._get_path(document_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path.as_uri()

    def get_document(self, document_id: DocumentId) -> BinaryIO:
        return self._get_path(document_id).open("rb")

    def _get_path(self, id_: UUID) -> Path:
        return self._base_dir / self._dir / str(id_)
