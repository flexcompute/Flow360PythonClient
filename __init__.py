import os
import json
from . import mesh
from . import case
from .httputils import FileDoesNotExist

def newMesh(fname, noSlipWalls, meshName=None, tags=[],
            fmat=None, endianness=None):
    if not os.path.exists(fname):
        print('mesh file {0} does not Exist!'.format(fname), flush=True)
        raise FileDoesNotExist(fname)
    if meshName is None:
        meshName = os.path.basename(fname).split('.')[0]
    if fmat is None:
        if fname.endswith('.ugrid'):
            fmat = 'aflr3'
        else:
            raise RuntimeError('Unknown format for file {}'.format(fname))
    if endianness is None:
        try:
            if fname.split('.')[-2] == 'b8':
                endianness = 'big'
            elif fname.split('.')[-2] == 'lb8':
                endianness = 'little'
            else:
                raise
        except:
            raise RuntimeError('Unknown endianness for file {}'.format(fname))
    resp = mesh.AddMesh(meshName, noSlipWalls, tags, fmat, endianness)
    meshId = resp['meshId']
    mesh.UploadMesh(meshId, fname)
    return meshId

def newCase(meshId, config, caseName=None, tags=[],
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
    resp = case.SubmitCase(caseName, tags, meshId, priority, config, parentId)
    return resp['caseId']
