import json
from io import BytesIO
from typing import Any

import boto3

from peakventures.credentials import get_credentials_json, S3_CREDENTIALS_NAME

CONTAINER_NAME = "models"


def _store_model_s3(name: str, payload: str) -> None:
    credentials = get_credentials_json(S3_CREDENTIALS_NAME)

    s3 = boto3.client(
        "s3",
        endpoint_url=credentials["endpoint_url"],
        aws_access_key_id=credentials["access_key_id"],
        aws_secret_access_key=credentials["secret_access_key"],
    )

    with BytesIO(payload.encode("utf-8")) as buffer:
        s3.upload_fileobj(buffer, CONTAINER_NAME, name)


def store_model(name: str, payload: Any) -> None:
    """Store model on the remote storage."""
    json_payload = json.dumps(payload)

    _store_model_s3(name, json_payload)


__all__ = [
    "store_model"
]
