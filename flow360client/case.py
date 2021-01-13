import json
import time

from . import mesh
from .authentication import refreshToken
from .httputils import post2, delete2, get2
from .s3utils import s3Client
from .config import Config
auth = Config.auth
keys = Config.user

@refreshToken
def SubmitCase(name, tags, meshId, priority, config, parentId=None):
    body = {
        "name": name,
        "tags": tags,
        "meshId" : meshId,
        "priority" : priority,
        "runtimeParams": config,
        "parentId": parentId
    }

    url = f'mesh/{meshId}/case'

    resp = post2(url, data=body)
    return resp


@refreshToken
def DeleteCase(caseId):

    url = f'case/{caseId}'
    resp = delete2(url)
    return resp


@refreshToken
def GetCaseInfo(caseId):

    url = f'case/{caseId}'

    resp = get2(url)
    runtime = get2(f'case/{caseId}/runtimeParams')
    runtimeContent = None
    try:
        runtimeContent = json.loads(runtime['content'])
    except Exception as e:
        print('invalid runtimeParams or not exist:' + runtime['content'])
        return None

    resp['runtimeParams'] = runtimeContent
    return resp

@refreshToken
def ListCases(name=None, status=None, meshId=None, include_deleted=False):
    if meshId is None:
        url = "cases"
    else:
        url = f'mesh/{meshId}/cases'

    resp = get2(url)
    if not include_deleted:
        resp = list(filter(lambda i : i['caseStatus'] != 'deleted', resp))
    return resp

@refreshToken
def GetCaseResidual(caseId):

    url = f'case/{caseId}/residual'
    resp = get2(url)
    return resp

@refreshToken
def GetCaseTotalForces(caseId):
    url = f'case/{caseId}/totalForces'
    resp = get2(url)
    return resp

@refreshToken
def GetCaseSurfaceForces(caseId, surfaces):
    try:
        obj = s3Client.get_object(Bucket=Config.CASE_BUCKET,
                                  Key='users/{0}/{1}/results/{2}'.format(keys['UserId'], caseId, 'surface_forces.csv'))
        data = obj['Body'].read().decode('utf-8')
    except Exception as e:
        print('no surface forces available')
        return None

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
# caseId: case uuid to retrieve case
# surfaces: the sorted list of surface names
def GetCaseSurfaceForcesByNames(caseId, surfaces):

    caseInfo = GetCaseInfo(caseId)
    # print(caseInfo)
    meshInfo = mesh.GetMeshInfo(caseInfo['caseMeshId'])
    boundaryNames = meshInfo['boundaries']
    print('fetch the name of boundaries:\n')
    print(boundaryNames)
    if boundaryNames is None or len(boundaryNames) == 0:
        raise RuntimeError('the boundaries name is empty, please re-process the mesh to populate the data')

    try:
        obj = s3Client.get_object(Bucket=Config.CASE_BUCKET,
                                  Key='users/{0}/{1}/results/{2}'.format(keys['UserId'], caseId, 'surface_forces.csv'))
        data = obj['Body'].read().decode('utf-8')
    except Exception as e:
        print('no surface forces available')
        return None


    headerKeys = ['steps',
                  'CL', 'CD', 'CFx', 'CFy', 'CFz', 'CMx', 'CMy', 'CMz',
                  'CLPressure', 'CDPressure', 'CFxPressure', 'CFyPressure', 'CFzPressure', 'CMxPressure', 'CMyPressure', 'CMzPressure',
                  'CLViscous', 'CDViscous', 'CFxViscous', 'CFyViscous', 'CFzViscous', 'CMxViscous', 'CMyViscous', 'CMzViscous']

    headers, forces = readCSV(data)
    resp = {}

    for surfaceName in surfaces:
        surfaceId = boundaryNames.index(surfaceName)

        if int(surfaceId) <= (len(forces)-1)/24:
            surfaceForces = assignCSVHeaders(headerKeys, forces, int(surfaceId)-1)
            resp[surfaceName] = surfaceForces
        else:
            print('surfaceId={0} is out of range. Max surface id should be {1}'.format(surfaceId, int(len(forces)-1)/24-1))
            raise RuntimeError('indexOutOfRange')

    return resp

@refreshToken
def DownloadResultsFile(caseId, src, target=None):
    if target is None:
        target = src
    if src is None:
        print('src fileName must not be None!')
        return
    s3Client.download_file(Bucket=Config.CASE_BUCKET,
                         Filename=target,
                         Key='users/{0}/{1}/results/{2}'.format(keys['UserId'], caseId, src))


@refreshToken
def DownloadVolumetricResults(caseId, fileName=None):
    if fileName is None:
        fileName = "volumes.tar.gz"
    if fileName[-7:] != '.tar.gz':
        print('fileName must have extension .tar.gz!')
        return
    DownloadResultsFile(caseId, "volumes.tar.gz", fileName)

@refreshToken
def DownloadSurfaceResults(caseId, fileName=None):
    if fileName is None:
        fileName = "surfaces.tar.gz"

    if fileName is not None and fileName[-7:] != '.tar.gz':
        print('fileName must have extension .tar.gz!')
        return

    DownloadResultsFile(caseId, "surfaces.tar.gz", fileName)

@refreshToken
def DownloadSolverOut(caseId, fileName=None):
    if fileName is None:
        fileName = 'solver.out'
    s3Client.download_file(Bucket=Config.CASE_BUCKET,
                           Filename=fileName,
                           Key='users/{0}/{1}/{2}'.format(keys['UserId'], caseId, 'solver.out'))

def WaitOnCase(caseId, timeout=86400, sleepSeconds=10):
    startTime = time.time()
    while time.time() - startTime < timeout:
        try:
            info = GetCaseInfo(caseId)
            if info['caseStatus'] in ['error', 'unknownError', 'completed']:
                return info['caseStatus']
        except Exception as e:
            print('Warning : {0}'.format(str(e)))

        time.sleep(sleepSeconds)

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
