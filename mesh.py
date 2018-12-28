import boto3
import time
import requests
import os
import json
import sys
from authentication import *
from httputils import post, get, delete

boto3.setup_default_session(region_name='us-east-1')

class FileDoesNotExist(Exception):
    pass

flow360url = 'https://dsxjn7ioqe.execute-api.us-gov-west-1.amazonaws.com/beta-1'
s3Client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key,
    region_name = 'us-gov-west-1'
)

@refreshToken
def AddMesh(name, noSlipWalls, tags, fmat, endianness):
    body = {
        "name": name,
        "tags": tags,
        "format" : fmat,
        "endianness" : endianness,
        "noSlipWalls" : noSlipWalls,
    }
    
    url = flow360url + '/add-mesh'

    resp = post(url, auth=auth, data=json.dumps(body))
    return resp

@refreshToken
def DeleteMesh(meshId):
    params = {
        "meshId": meshId,
    }
    
    url = flow360url + '/delete-mesh'

    resp = delete(url, auth=auth, params=params)
    return resp

@refreshToken
def GetMeshInfo(meshId):
    params = {
        "meshId": meshId,
    }
    
    url = flow360url + '/get-mesh-info'

    resp = get(url, auth=auth, params=params)
    return resp

@refreshToken
def ListMeshes(name=None, status=None):
    params = {
        "name": name,
        "status": status,
    }
    
    url = flow360url + '/list-meshes'

    resp = get(url, auth=auth, params=params)
    return resp

class UploadProgress(object):

    def __init__(self, size):
        self.size = size
        self.uploadedSoFar = 0

    def report(self, bytes_in_chunk):
        self.uploadedSoFar += bytes_in_chunk
        sys.stdout.write('\rfile upload progress: {0:2.2f} %'.format(float(self.uploadedSoFar)/self.size*100))
        sys.stdout.flush()

@refreshToken
def UploadMesh(meshId, meshFile):
    def getMeshName(meshFile, meshFormat, endianness):
        if meshFormat == 'aflr3':
            if endianness == 'big':
                name = 'mesh.b8.ugrid'
            elif endianness == 'little':
                name ='mesh.lb8.ugrid'
            else:
                raise RuntimeError("unknown endianness: {}".format(endianness))
        else:
            raise RuntimeError("unknown meshFormat: {}".format(meshFormat))
        if meshFile.endswith('.gz'):
            name += '.gz'
        elif meshFile.endswith('.bz2'):
            name += '.bz2'
        return name

    meshInfo = GetMeshInfo(meshId)
    print(meshInfo)
    fileName = getMeshName(meshFile, meshInfo['format'],
                           meshInfo['endianness'])
    
    if not os.path.exists(meshFile):
        print('mesh file {0} does not Exist!'.format(meshFile))
        raise FileDoesNotExist(meshFile)

    fileSize = os.path.getsize(meshFile)
    prog = UploadProgress(fileSize)
    #s3Client.upload_file(Bucket='flow360meshes',
    #                     Filename=meshFile,
    #                     Key='users/{0}/meshes/{1}/{2}'.format(creds['IdentityId'], meshId, fileName),
    #                     Callback = prog.report)
    s3Client.upload_file(Bucket='flow360meshes',
                         Filename=meshFile,
                         Key='users/{0}/{1}/{2}'.format(user_id, meshId, fileName),
                         Callback = prog.report)
    print()
