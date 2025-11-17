import boto3
from app.config.settings import Settings

runtime = boto3.client(
    "bedrock-agent-runtime",
    aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
    region_name=Settings.AWS_DEFAULT_REGION
)

def retrieve_context(query, top_k=3):
    response = runtime.retrieve(
        knowledgeBaseId=Settings.KNOWLEDGE_BASE_ID,
        retrievalQuery={"text": query},
        retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": top_k}}
    )
    return response["retrievalResults"]
