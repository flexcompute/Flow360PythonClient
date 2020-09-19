import sys

import boto3
from .config import Config
keys = Config.user
s3Client = boto3.client(
    's3',
    aws_access_key_id=keys['userAccessKey'],
    aws_secret_access_key=keys['userSecretAccessKey'],
    region_name=Config.S3_REGION
)

class UploadProgress(object):

    def __init__(self, size):
        self.size = size
        self.uploadedSoFar = 0

    def report(self, bytes_in_chunk):
        self.uploadedSoFar += bytes_in_chunk
        sys.stdout.write('\rfile upload progress: {0:2.2f} %'.format(float(self.uploadedSoFar)/self.size*100))
        sys.stdout.flush()