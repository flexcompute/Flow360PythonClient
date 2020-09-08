import boto3
from .config import Config
keys = Config.user
s3Client = boto3.client(
    's3',
    aws_access_key_id=keys['userAccessKey'],
    aws_secret_access_key=keys['userSecretAccessKey'],
    region_name=Config.S3_REGION
)