import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
    AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    KNOWLEDGE_BASE_ID = "KKMQULBTIX"
    DATA_SOURCE_ID = "QHOXJA8BHP"
    S3_PREFIX = "reports/"
