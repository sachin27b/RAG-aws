import time
import logging
import boto3
from app.config.settings import Settings

logger = logging.getLogger("INGEST")

bedrock = boto3.client(
    "bedrock-agent",
    aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
    region_name=Settings.AWS_DEFAULT_REGION
)

def start_ingestion():
    resp = bedrock.start_ingestion_job(
        knowledgeBaseId=Settings.KNOWLEDGE_BASE_ID,
        dataSourceId=Settings.DATA_SOURCE_ID
    )
    job_id = resp["ingestionJob"]["ingestionJobId"]
    logger.info(f"Ingestion started: {job_id}")
    return job_id


def wait_for_ingestion(job_id):
    while True:
        status = bedrock.get_ingestion_job(
            knowledgeBaseId=Settings.KNOWLEDGE_BASE_ID,
            dataSourceId=Settings.DATA_SOURCE_ID,
            ingestionJobId=job_id
        )["ingestionJob"]["status"]

        logger.info(f"Status: {status}")

        if status in ["COMPLETE", "FAILED"]:
            return status

        time.sleep(10)
