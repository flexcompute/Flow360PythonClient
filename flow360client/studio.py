import os

from boto3.s3.transfer import TransferConfig

from flow360client.httputils import get2, put2, post2, delete2
from .authentication import refreshToken
from .config import Config
from .s3utils import s3Client, UploadProgress

auth = Config.auth
keys = Config.user
@refreshToken
def UploadStudioItem(itemId, file):
    path, filename = os.path.split(file)
    fileSize = os.path.getsize(file)
    prog = UploadProgress(fileSize)
    key = 'users/{0}/{1}/{2}'.format(keys['userId'], itemId, filename)
    config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10,
                            multipart_chunksize=1024 * 25, use_threads=True)

    s3Client.upload_file(Bucket=Config.STUDIO_BUCKET,
                         Filename=file,
                         Key=key,
                         Callback=prog.report,
                         Config=config)
    item = {
        'itemId': str(itemId),
        'status': 'processed',
        's3Path': key
    }

    return UpdateStudioItem(item)

def UpdateStudioItem(item):
    return put2(f'studio/item/{item["itemId"]}', item)


def NewStudioItem(item):
    return post2(f'studio/item', item)

def GetStudioItem(itemId):
    return get2(f'studio/item/{itemId}')

def DeleteStudioItem(itemId):
    return delete2(f'studio/item/{itemId}')

def CopyResourceToMesh(itemId, meshId):
    return post2(f'studio/item/{itemId}/copyToMesh/{meshId}')



