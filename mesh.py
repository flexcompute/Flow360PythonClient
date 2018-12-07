import boto3
import time
import requests
import os
import json
import sys
from authentication import getCredentials, getAPIAuthentication
from httputils import post, get, delete

boto3.setup_default_session(region_name='us-east-1')

class FileDoesNotExist(Exception):
    pass

def email2username(email):
    return email.replace('@','-at-')

creds = getCredentials(email2username('youremail'),
                       'yourpassword')

auth = getAPIAuthentication(creds)

flow360url = 'https://zcvxbr69d2.execute-api.us-east-1.amazonaws.com/beta'

s3Client = boto3.client(
    's3',
    aws_access_key_id=creds['Credentials']['AccessKeyId'],
    aws_secret_access_key=creds['Credentials']['SecretKey'],
    aws_session_token=creds['Credentials']['SessionToken'],
)

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

def DeleteMesh(meshId):
    params = {
        "meshId": meshId,
    }
    
    url = '{0}/{1}'.format(flow360url, 'delete-mesh')

    resp = delete(url, auth=auth, params=params)
    return resp

def GetMeshInfo(meshId):
    params = {
        "meshId": meshId,
    }
    
    url = '{0}/{1}'.format(flow360url, 'get-mesh-info')

    resp = get(url, auth=auth, params=params)
    return resp

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

def UploadMesh(meshId, meshFile):
    fileName = os.path.basename(meshFile)
    if not os.path.exists(meshFile):
        print('mesh file {0} does not Exist!'.format(meshFile))
        raise FileDoesNotExist(meshFile)

    fileSize = os.path.getsize(meshFile)
    prog = UploadProgress(fileSize)
    s3Client.upload_file(Bucket='flow360data',
                         Filename=meshFile,
                         Key='users/{0}/meshes/{1}/{2}'.format(creds['IdentityId'], meshId, fileName),
                         Callback = prog.report)
