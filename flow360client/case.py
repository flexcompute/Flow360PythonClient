import json
import time
from .authentication import auth, keys, refreshToken
from .httputils import post, get, delete, flow360url
from .s3utils import s3Client

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
def GetCaseSurfaceForces(caseId, surfaces):
    try:
        obj = s3Client.get_object(Bucket='flow360cases',
                                  Key='users/{0}/{1}/results/{2}'.format(keys['UserId'], caseId, 'surface_forces.csv'))
        data = obj['Body'].read().decode('utf-8')
    except Exception as e:
        print('no surface forces available')
        return None

    def readCSV(d):
        data = [[x for x in l.split(', ') if x] for l in d.split('\n')]
        ncol = len(data[0])
        nrow = len(data)
        new = [[float(data[i][c]) for i in range(1,nrow) if len(data[i])] for c in range(0,ncol)]
        return (data[0], new)

    def assignCSVHeaders(keys, arrays, surfaceId):
        response = {}
        for idx, key in enumerate(keys):
            if key=='steps':
                response[key] = arrays[0]
            else:
                response[key] = arrays[idx + surfaceId*24]
        return response

    headerKeys = ['steps',
                  'CL', 'CD', 'CFx', 'CFy', 'CFz', 'CMx', 'CMy', 'CMz',
                  'CLPressure', 'CDPressure', 'CFxPressure', 'CFyPressure', 'CFzPressure', 'CMxPressure', 'CMyPressure', 'CMzPressure',
                  'CLViscous', 'CDViscous', 'CFxViscous', 'CFyViscous', 'CFzViscous', 'CMxViscous', 'CMyViscous', 'CMzViscous']


    headers, forces = readCSV(data)
    resp = {}
    for surface in surfaces:
        surfaceIds = surface['surfaceIds']
        surfaceName = surface['surfaceName']
        allSurfaceForces = {}
        for headerKey in headerKeys:
            allSurfaceForces[headerKey] = [0]*len(forces[0])

        for surfaceId in surfaceIds:
            if int(surfaceId) <= (len(forces)-1)/24:
                surfaceForces = assignCSVHeaders(headerKeys, forces, int(surfaceId)-1)
                for headerKey in headerKeys[1:]:
                    allSurfaceForces[headerKey] = [i + j for i, j in zip(allSurfaceForces[headerKey], surfaceForces[headerKey])]
                allSurfaceForces['steps'] = surfaceForces['steps']
            else:
                print('surfaceId={0} is out of range. Max surface id should be {1}'.format(surfaceId, int(len(forces)-1)/24-1))
                raise RuntimeError('indexOutOfRange')
        resp[surfaceName] = allSurfaceForces

    return resp


@refreshToken
def DownloadVolumetricResults(caseId, fileName):
    if fileName[-7:] != '.tar.gz':
        print('fileName must have extension .tar.gz!')
        return
    s3Client.download_file(Bucket='flow360cases',
                         Filename=fileName,
                         Key='users/{0}/{1}/results/{2}'.format(keys['UserId'], caseId, 'vtu.tar.gz'))

@refreshToken
def DownloadSurfaceResults(caseId, fileName):
    if fileName[-7:] != '.tar.gz':
        print('fileName must have extension .tar.gz!')
        return
    s3Client.download_file(Bucket='flow360cases',
                         Filename=fileName,
                         Key='users/{0}/{1}/results/{2}'.format(keys['UserId'], caseId, 'surfaces.tar.gz'))

@refreshToken
def DownloadCaseResults(caseId, fileName):
    DownloadVolumetricResults(caseId, fileName)

@refreshToken
def DownloadSolverOut(caseId):
    s3Client.download_file(Bucket='flow360cases',
                           Filename='solver.out',
                           Key='users/{0}/{1}/results/{2}'.format(keys['UserId'], caseId, 'solver.out'))

def WaitOnCase(caseId, timeout=86400, sleepSeconds=10):
    startTime = time.time()
    while time.time() - startTime < timeout:
        try:
            info = GetCaseInfo(caseId)
            if info['status'] in ['error', 'unknownError', 'completed']:
                return info['status']
        except Exception as e:
            print('Warning : {0}'.format(str(e)))

        time.sleep(sleepSeconds)
