import boto3
import time
import requests
import os
import json
import sys
from authentication import auth, refreshToken
from httputils import post, get, delete, s3Client
from httputils import FileDoesNotExist


@refreshToken
def AddMesh(name, noSlipWalls, tags, fmat, endianness):
    body = {
        "name": name,
        "tags": tags,
        "format" : fmat,
        "endianness" : endianness,
        "noSlipWalls" : noSlipWalls,
    }
    
    url = '{0}/{1}'.format(flow360url, 'add-mesh')

    resp = post(url, auth=auth, data=json.dumps(body))
    return resp

@refreshToken
def DeleteMesh(meshId):
    params = {
        "meshId": meshId,
    }
    
    url = '{0}/{1}'.format(flow360url, 'delete-mesh')

    resp = delete(url, auth=auth, params=params)
    return resp

@refreshToken
def GetMeshInfo(meshId):
    params = {
        "meshId": meshId,
    }
    
    url = '{0}/{1}'.format(flow360url, 'get-mesh-info')

    resp = get(url, auth=auth, params=params)
    return resp

@refreshToken
def ListMeshes(name=None, status=None):
    params = {
        "name": name,
        "status": status,
    }
    
    url = '{0}/{1}'.format(flow360url, 'list-meshes')

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
def UploadMesh(meshId, meshFile, meshFormat='ugrid', endianness='big'):
    def getMeshName(meshFile, meshFormat, endianness):
        if meshFormat == 'ugrid':
            if endianness == 'big':
                return 'mesh.b8.ugrid'
            else:
                return  'mesh.lb8.ugrid'

    if meshFormat != 'ugrid':
        raise RuntimeError('Invalid mesh type: {0}'.format(meshFormat))

    if endianness not in ['big', 'litte']:
        raise RuntimeError('Invalid mesh endianness: {0}!'.format(endianness))

    fileName = getMeshName(meshFile, meshFormat, endianness)
    
    if not os.path.exists(meshFile):
        print('mesh file {0} does not Exist!'.format(meshFile))
        raise FileDoesNotExist(meshFile)

    fileSize = os.path.getsize(meshFile)
    prog = UploadProgress(fileSize)
    s3Client.upload_file(Bucket='flow360meshes',
                         Filename=meshFile,
                         Key='users/{0}/{1}/{2}'.format(user_id, meshId, fileName),
                         Callback = prog.report)
