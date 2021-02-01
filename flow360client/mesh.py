import json
import os
import time
from os.path import getsize

from boto3.s3.transfer import TransferConfig
from .authentication import refreshToken
from .httputils import post2, get2, put2, delete2
from .s3utils import s3Client, UploadProgress
from .httputils import FileDoesNotExist
from .config import Config
auth = Config.auth
keys = Config.user


@refreshToken
def AddMeshWithJson(name, mesh_json, tags, fmat, endianness, solver_version):
    return AddMeshBase(name, mesh_json, tags, fmat, endianness, solver_version)



@refreshToken
def AddMesh(name, noSlipWalls, tags, fmat, endianness, solver_version):

    return AddMeshBase(name, {
            "boundaries":
                {
                    "noSlipWalls": noSlipWalls
                }
        }, tags, fmat, endianness, solver_version)


def AddMeshBase(name, meshParams, tags, fmat, endianness, solver_version):
    '''
       AddMesh(name, noSlipWalls, tags, fmat, endianness, version)
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
        "meshName": name,
        "meshTags": tags,
        "meshFormat": fmat,
        "meshEndianness": endianness,
        "meshParams": json.dumps(meshParams),

    }

    if solver_version:
        body['solverVersion'] = solver_version

    resp = post2("mesh", data=body)
    return resp


@refreshToken
def DeleteMesh(meshId):
    resp = delete2(f"mesh/{meshId}")
    return resp

@refreshToken
def GetMeshInfo(meshId):
    url = f"mesh/{meshId}"
    resp = get2(url)
    return resp

@refreshToken
def UpdateMesh(meshInfo):
    url = f"mesh/{meshInfo['meshId']}"
    resp = put2(url, meshInfo)
    return resp

@refreshToken
def ListMeshes(include_deleted=False):

    resp = get2("meshes")
    if not include_deleted:
        resp = list(filter(lambda i: i['meshStatus'] != 'deleted', resp))
    return resp


@refreshToken
def UploadMesh(meshId, meshFile):
    '''
    UploadMesh(meshId, meshFile)
    '''
    def getMeshName(meshFile, meshName, meshFormat, endianness):
        if meshFormat == 'aflr3':
            if endianness == 'big':
                name = 'mesh.b8.ugrid'
            elif endianness == 'little':
                name ='mesh.lb8.ugrid'
            else:
                raise RuntimeError("unknown endianness: {}".format(endianness))
        else:
            name = meshName
            if not name.endswith(meshFormat):
                name += '.' + meshFormat

        if meshFile.endswith('.gz'):
            name += '.gz'
        elif meshFile.endswith('.bz2'):
            name += '.bz2'
        return name

    meshInfo = GetMeshInfo(meshId)
    print(meshInfo)
    fileName = getMeshName(meshFile, meshInfo['meshName'], meshInfo['meshFormat'],
                           meshInfo['meshEndianness'])

    if not os.path.exists(meshFile):
        print('mesh file {0} does not Exist!'.format(meshFile))
        raise FileDoesNotExist(meshFile)

    fileSize = os.path.getsize(meshFile)
    prog = UploadProgress(fileSize)
    config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10,
                            multipart_chunksize=1024 * 25, use_threads=True)

    s3Client.upload_file(Bucket=Config.MESH_BUCKET,
                         Filename=meshFile,
                         Key='users/{0}/{1}/{2}'.format(keys['userId'], meshId, fileName),
                         Callback=prog.report,
                         Config=config)
    meshInfo['meshStatus'] = 'uploaded'
    meshInfo['meshCompression'] = getFileCompression(fileName)
    meshInfo['meshSize'] = getsize(meshFile)
    UpdateMesh(meshInfo)

@refreshToken
def DownloadMeshProc(meshId, fileName=None):
    if fileName == None:
        fileName = 'meshproc.out'
    s3Client.download_file(Bucket=Config.MESH_BUCKET,
                           Filename=fileName,
                           Key='users/{0}/{1}/info/{2}'.format(keys['userId'], meshId, 'meshproc.out'))


def WaitOnMesh(meshId, timeout=86400, sleepSeconds=10):
    startTime = time.time()
    while time.time() - startTime < timeout:
        try:
            info = GetMeshInfo(meshId)
            if info['meshStatus'] in ['error', 'unknownError', 'processed']:
                return info['meshStatus']
        except Exception as e:
            print('Warning : {0}'.format(str(e)))

        time.sleep(sleepSeconds)


def getFileCompression(name):
    if name.endswith("tar.gz"):
        return 'tar.gz'
    elif name.endswith(".gz"):
        return 'gz'
    elif name.endswith("bz2"):
        return 'bz2'
    else:
        return None
