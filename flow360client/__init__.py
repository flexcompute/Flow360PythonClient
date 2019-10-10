import os
import json
import flow360client.mesh
import flow360client.case
from flow360client.httputils import FileDoesNotExist
from flow360client.fun3d_to_flow360 import translate_boundaries
from flow360client.httputils import FileDoesNotExist

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
    resp = case.SubmitCase(caseName, tags, meshId, priority, config, parentId)
    return resp['caseId']

def NewMesh(fname, noSlipWalls, meshName=None, tags=[],
            fmat=None, endianness=None, solverVersion=None):
    if not os.path.exists(fname):
        print('mesh file {0} does not Exist!'.format(fname), flush=True)
        raise FileDoesNotExist(fname)
    if meshName is None:
        meshName = os.path.basename(fname).split('.')[0]
    if fmat is None:
        if fname.endswith('.ugrid') or fname.endswith('.ugrid.gz') or \
           fname.endswith('.ugrid.bz2'):
            fmat = 'aflr3'
        else:
            raise RuntimeError('Unknown format for file {}'.format(fname))
    if endianness is None:
        try:
            if fname.find('.b8.') != -1:
                endianness = 'big'
            elif fname.find('.lb8.') != -1:
                endianness = 'little'
            else:
                raise
        except:
            raise RuntimeError('Unknown endianness for file {}'.format(fname))
    resp = mesh.AddMesh(meshName, noSlipWalls, tags, fmat, endianness, solverVersion)
    meshId = resp['meshId']
    mesh.UploadMesh(meshId, fname)
    print()
    return meshId

def noSlipWallsFromMapbc(mapbcFile):
    assert mapbcFile.endswith('.mapbc') == True
    if not os.path.exists(mapbcFile):
        print('mapbc file {0} does not exist'.format(mapbcFile))
        raise RuntimeError('FileNotFound')
    with open(mapbcFile, 'r') as f:
        mapbc = f.read()
    bc, noslipWalls = translate_boundaries(mapbc)
    return noslipWalls
