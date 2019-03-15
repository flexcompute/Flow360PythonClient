import boto3
from flow360client.authentication import keys

s3Client = boto3.client(
    's3',
    aws_access_key_id=keys['UserAccessKey'],
    aws_secret_access_key=keys['UserSecretAccessKey'],
    region_name = 'us-gov-west-1'
)