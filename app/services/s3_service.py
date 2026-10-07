import io

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.core.config import settings


s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)


def upload_file_to_s3(
    file_content: bytes,
    object_key: str,
    content_type: str,
):
    try:
        s3_client.put_object(
            Bucket=settings.AWS_S3_BUCKET_NAME,
            Key=object_key,
            Body=file_content,
            ContentType=content_type,
        )

        return object_key

    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(
            "Failed to upload document to S3."
        ) from exc


def download_file_from_s3(
    object_key: str,
) -> bytes:
    buffer = io.BytesIO()

    try:
        s3_client.download_fileobj(
            settings.AWS_S3_BUCKET_NAME,
            object_key,
            buffer,
        )

        buffer.seek(0)

        return buffer.read()

    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(
            "Failed to download document from S3."
        ) from exc


def delete_file_from_s3(
    object_key: str,
):
    try:
        s3_client.delete_object(
            Bucket=settings.AWS_S3_BUCKET_NAME,
            Key=object_key,
        )

    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(
            "Failed to delete document from S3."
        ) from exc


def generate_presigned_url(
    object_key: str,
    expiration: int = 300,
):
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": settings.AWS_S3_BUCKET_NAME,
                "Key": object_key,
            },
            ExpiresIn=expiration,
        )

    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(
            "Failed to generate document access URL."
        ) from exc