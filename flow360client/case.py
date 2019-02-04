import boto3
import time
import requests
import os
import json
import sys
from .authentication import auth, keys, refreshToken
from .httputils import post, get, delete, s3Client, flow360url
from .httputils import FileDoesNotExist

@refreshToken
def SubmitCase(name, tags, meshId, priority, config, parentId=None):
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
def ListCases(name=None, status=None, meshId=None, include_deleted=False):
    params = {
        "name": name,
        "status": status,
        "meshId" : meshId
    }

    url = '{0}/{1}'.format(flow360url, 'list-cases')

    resp = get(url, auth=auth, params=params)
    if not include_deleted:
        resp = list(filter(lambda i : i['status'] != 'deleted', resp))
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

@refreshToken
def DownloadCaseResults(caseId, fileName):
    if fileName[-7:] != '.tar.gz':
        print('fileName must have extension .tar.gz!')
        return
    s3Client.download_file(Bucket='flow360cases',
                         Filename=fileName,
                         Key='users/{0}/{1}/results/{2}'.format(keys['UserId'], caseId, 'vtu.tar.gz'))

def NewCase(meshId, config, caseName=None, tags=[],
            priority='low', parentId=None):
    if isinstance(config, str):
        if not os.path.exists(config):
            print('config file {0} does not Exist!'.format(config), flush=True)
            raise FileDoesNotExist(config)
        if caseName is None:
            caseName = os.path.basename(config).split('.')[0]
        config = json.load(open(config))
    assert isinstance(config, dict)
    assert caseName is not None
    resp = SubmitCase(caseName, tags, meshId, priority, config, parentId)
    return resp['caseId']
