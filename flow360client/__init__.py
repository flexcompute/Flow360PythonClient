import math
import os
import json
import sys
import uuid
from os.path import basename

import flow360client.mesh
import flow360client.case
from flow360client.config import Config
from flow360client.httputils import FileDoesNotExist, post2
from flow360client.fun3d_to_flow360 import translate_boundaries
from flow360client.httputils import FileDoesNotExist
from flow360client.studio import UploadStudioItem, NewStudioItem
from flow360client.task import NewTask, GetTask, WaitOnTask


def NewCase(meshId, config, caseName=None, tags=[],
            priority='high', parentId=None):
    if isinstance(config, str):
        if not os.path.exists(config):
            print('config file {0} does not Exist!'.format(config), flush=True)
            raise FileDoesNotExist(config)
        if caseName is None:
            caseName = os.path.basename(config).split('.')[0]
        config = json.load(open(config))
    assert isinstance(config, dict)
    assert caseName is not None
    resp = case.SubmitCase(caseName, tags, meshId, priority, json.dumps(config), parentId)
    return resp['caseId']


def NewCaseListWithPhase(meshId, config, caseName=None, tags=[],
                         priority='high', parentId=None, phaseCount=1):
    if isinstance(config, str):
        if not os.path.exists(config):
            print('config file {0} does not Exist!'.format(config), flush=True)
            raise FileDoesNotExist(config)
        if caseName is None:
            caseName = os.path.basename(config).split('.')[0]
        config = json.load(open(config))
    assert isinstance(config, dict)
    assert caseName is not None
    assert phaseCount >= 1
    caseIds = []
    totalSteps = config['timeStepping']['maxPhysicalSteps']
    phaseSteps = math.ceil(totalSteps / phaseCount)
    index = 1

    while totalSteps > 0:
        config['timeStepping']['maxPhysicalSteps'] = min(totalSteps, phaseSteps)
        resp = case.SubmitCase(f'{caseName}_{index}', tags, meshId, priority, json.dumps(config), parentId)
        caseIds.append(resp['caseId'])
        totalSteps = totalSteps - phaseSteps
        parentId = resp['caseId']
        index = index + 1
    return caseIds

def NewMesh(fname, noSlipWalls=None, meshName=None, tags=[],
            fmat=None, endianness=None, solverVersion=None, meshJson=None):
    if not os.path.exists(fname):
        print('mesh file {0} does not Exist!'.format(fname), flush=True)
        raise FileDoesNotExist(fname)
    if meshName is None:
        meshName = os.path.splitext(basename(fname))[0]

    if fmat is None:
        if fname.endswith('.ugrid') or fname.endswith('.ugrid.gz') or \
                fname.endswith('.ugrid.bz2'):
            fmat = 'aflr3'
        elif fname.endswith('.cgns') or fname.endswith('.cgns.gz') or \
                fname.endswith('.cgns.bz2'):
            fmat = 'cgns'
        else:
            raise RuntimeError('Unknown format for file {}'.format(fname))

    if endianness is None:
        try:
            if fname.find('.b8.') != -1:
                endianness = 'big'

            elif fname.find('.lb8.') != -1:
                endianness = 'little'
            else:
                endianness = ''
        except:
            raise RuntimeError('Unknown endianness for file {}'.format(fname))

    if noSlipWalls is None and meshJson is None:
        raise RuntimeError('Both noSlipWals or meshJson are none')

    if noSlipWalls is not None and meshJson is not None:
        noSlipWalls = None
        print('noSlipWalls will be override by meshJson')

    if noSlipWalls is not None:
        resp = mesh.AddMesh(meshName, noSlipWalls, tags, fmat, endianness, solverVersion)
    else:
        resp = mesh.AddMeshWithJson(meshName, meshJson, tags, fmat, endianness, solverVersion)

    meshId = resp['meshId']
    mesh.UploadMesh(meshId, fname)
    print()
    return meshId


def NewMeshWithTransform(fname, meshName=None, tags=[], solverVersion=None):
    if not solverVersion:
        solverVersion = Config.VERSION_CFD
    if not meshName:
        meshName = 'Flow360Mesh'
    with open(fname) as file:
        globalJson = json.load(file)
    transformsJson = globalJson["transforms"]
    meshFile = globalJson["mesh"]
    dirName = os.path.dirname(os.path.abspath(fname))
    transformingTasks = []

    sourceFiles = globalJson["sources"]
    fileToStudioItem = {}
    print("uploading source files")
    for filename in sourceFiles:

        item = UploadStudioItem(uuid.uuid1(), os.path.join(dirName, filename))
        print(item)
        fileToStudioItem[filename] = item


    for transformConfigFile in transformsJson:
        with open(os.path.join(dirName, transformConfigFile), 'r') as file:
            transformConfig = json.load(file)
            taskParam = json.dumps(transformConfig)
        filename = transformConfig['inputMesh']
        if filename in fileToStudioItem.keys():


            item = fileToStudioItem[filename]

            newItem = NewStudioItem({
                'status': "processing",
                'parentId': item['itemId'],
                's3Path': transformConfig['outputMesh']
            })

            task = {
                'taskParam': taskParam,
                'taskType': 'transform',
                'objectId': newItem['itemId'],
                'solverVersion': solverVersion
            }

            task = NewTask(task)
            print(task)
            transformingTasks.append(task)
        else:
            raise RuntimeError(f'the required file is not uploaded: \r {transformConfig["inputMesh"]}')

    transformingSize = len(transformingTasks)
    transformedSize = 0

    while transformedSize < transformingSize:
        for task in transformingTasks:
            status = WaitOnTask(task['taskId'])
            if status == 'success':
                transformedSize = transformedSize + 1
            elif status == 'error':
                raise RuntimeError(f'transformed failed for {task["objectId"]}: \r {task["taskParam"]}')
            sys.stdout.write(f'\r transformed {transformedSize} / {transformingSize}')
            sys.stdout.flush()

    # merge the files.
    parentIds = [x['objectId'] for x in transformingTasks] + [x['itemId'] for x in fileToStudioItem.values()]

    print(f"\r transformed {transformedSize} / {transformingSize}")
    print("\rstart merge process...")
    mergeJson = globalJson["merge"]
    item = {
        'status': "processing",
        'parentId': ','.join(parentIds),
        's3Path': f'{meshName}.meshmerged.json'
    }
    item = NewStudioItem(item)
    with open(os.path.join(dirName, mergeJson), 'r') as file:
        taskParam = file.read()
    task = {
        'taskType': "merge",
        'taskParam': taskParam,
        'objectId': item['itemId'],
        'solverVersion': solverVersion,
    }
    task = NewTask(task)

    print(f'merge.task:{task}')
    status = WaitOnTask(task['taskId'])
    if status == 'error':
        raise RuntimeError(f'merge failed: \r {task["taskParam"]}')
    with open(os.path.join(dirName, meshFile), 'r') as file:
        meshParam = file.read()

    mesh = {
        'meshName': f'{meshName}.meshmerged.json',
        'meshTags': tags,
        'meshFormat': '',
        'meshSize': 0,
        'meshParams': meshParam,
        'meshStatus': 'uploading',
        'solverVersion': solverVersion,
        'meshCompression': 'tar.gz'
    }

    finalMesh = post2("mesh", data=mesh)
    try:
        mesh = post2(f'studio/item/{item["itemId"]}/copyToMesh/{finalMesh["meshId"]}')
    except Exception as inst:
        print(inst.args)
    print("start mesh process on backend")
    print(finalMesh)
    return finalMesh


def noSlipWallsFromMapbc(mapbcFile):
    assert mapbcFile.endswith('.mapbc') == True
    if not os.path.exists(mapbcFile):
        print('mapbc file {0} does not exist'.format(mapbcFile))
        raise RuntimeError('FileNotFound')
    with open(mapbcFile, 'r') as f:
        mapbc = f.read()
    bc, noslipWalls = translate_boundaries(mapbc)
    return noslipWalls