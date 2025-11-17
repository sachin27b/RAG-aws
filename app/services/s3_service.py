import boto3
from app.config.settings import Settings
import logging

logger = logging.getLogger("S3")

s3 = boto3.client(
    "s3",
    aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
    region_name=Settings.AWS_DEFAULT_REGION
)

def upload_chunk(object_key, buffer):
    key = f"{Settings.S3_PREFIX}{object_key}"
    logger.info(f"Uploading: {key}")

    s3.upload_fileobj(buffer, Settings.AWS_BUCKET_NAME, key)
