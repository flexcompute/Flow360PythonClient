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

#flow360url = 'https://zcvxbr69d2.execute-api.us-east-1.amazonaws.com/beta'
flow360url = 'https://dsxjn7ioqe.execute-api.us-gov-west-1.amazonaws.com/beta-1'

s3Client = boto3.client(
    's3',
    aws_access_key_id=keys['UserAccessKey'],
    aws_secret_access_key=keys['UserSecretAccessKey'],
    region_name = 'us-gov-west-1'
)

@refreshToken
def SubmitCase(name, tags, meshId, priority, configFile, parentId=None):
    if not os.path.exists(configFile):
        print('config file {0} does not Exist!'.format(configFile))
        raise FileDoesNotExist(meshFile)
    with open(configFile,'r') as f:
        config = json.loads(f.read())
    body = {
        "name": name,
        "tags": tags,
        "meshId" : meshId,
        "priority" : priority,
        "runtimeParams" : config,
        "parentId" : parentId
    }
    
    url = '{0}/{1}'.format(flow360url, 'submit-case')

    resp = post(url, auth=auth, data=json.dumps(body))
    return resp

@refreshToken
def DeleteCase(caseId):
    params = {
        "caseId": caseId,
    }
    
    url = '{0}/{1}'.format(flow360url, 'delete-case')

    resp = delete(url, auth=auth, params=params)
    return resp

@refreshToken
def GetCaseInfo(caseId):
    params = {
        "caseId": caseId,
    }
    
    url = '{0}/{1}'.format(flow360url, 'get-case-info')

    resp = get(url, auth=auth, params=params)
    return resp

@refreshToken
def PauseResumeCase(caseId, action):
    data = {
        "caseId": caseId,
        "action" : action
    }
    
    url = '{0}/{1}'.format(flow360url, 'pause-resume-case')

    resp = post(url, auth=auth, data=json.dumps(data))
    return resp

@refreshToken
def ListCases(name=None, status=None, meshId=None):
    params = {
        "name": name,
        "status": status,
        "meshId" : meshId
    }
    
    url = '{0}/{1}'.format(flow360url, 'list-cases')

    resp = get(url, auth=auth, params=params)
    return resp

@refreshToken
def GetCaseResidual(caseId):
    params = {
        "caseId" : caseId
    }
    
    url = '{0}/{1}'.format(flow360url, 'get-case-residual')

    resp = get(url, auth=auth, params=params)
    return resp

@refreshToken
def GetCaseTotalForces(caseId):
    params = {
        "caseId" : caseId
    }
    
    url = '{0}/{1}'.format(flow360url, 'get-case-total-forces')

    resp = get(url, auth=auth, params=params)
    return resp

@refreshToken
def GetCaseSurfaceForces(caseId, surfaceIds):
    params = {
        "caseId" : caseId
    }

    body = {
        "surfaceIds" : surfaceIds
    }
    
    url = '{0}/{1}'.format(flow360url, 'get-case-surface-forces')

    resp = post(url, auth=auth, data=json.dumps(body), params=params)
    return resp

