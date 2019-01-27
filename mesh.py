import boto3
import time
import requests
import os
import json
import sys
from authentication import auth, keys, refreshToken
from httputils import post, get, delete, s3Client
from httputils import FileDoesNotExist, flow360url
from boto3.s3.transfer import TransferConfig

@refreshToken
def AddMesh(name, noSlipWalls, tags, fmat, endianness):
    '''
    AddMesh(name, noSlipWalls, tags, fmat, endianness)
    returns the raw HTTP response
    {
        'meshId' : 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
        'addTime' : '2019:01:01:01:01:01.000000'
    }
    The returned meshId is need to subsequently call UploadMesh
    Example:
        resp = AddMesh('foo', [1], [], 'aflr3', 'big')
        UploadMesh(resp['meshId'], 'mesh.lb8.ugrid')
    '''
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
    '''
    UploadMesh(meshId, meshFile)
    '''
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
    config = TransferConfig()
    #config = TransferConfig(multipart_chunksize=33554432,
    #                        max_concurrency=100)
    config = TransferConfig(max_concurrency=100)

    s3Client.upload_file(Bucket='flow360meshes',
                         Filename=meshFile,
                         Key='users/{0}/{1}/{2}'.format(keys['UserId'], meshId, fileName),
                         Callback = prog.report,
                         Config=config)
