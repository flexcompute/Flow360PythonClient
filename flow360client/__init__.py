import os
import json
from flow360client.httputils import FileDoesNotExist
import flow360client.mesh
import flow360client.case

from flow360client.httputils import FileDoesNotExist

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
    resp = case.SubmitCase(caseName, tags, meshId, priority, config, parentId)
    return resp['caseId']

def NewMesh(fname, noSlipWalls, meshName=None, tags=[],
            fmat=None, endianness=None):
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
    resp = mesh.AddMesh(meshName, noSlipWalls, tags, fmat, endianness)
    meshId = resp['meshId']
    mesh.UploadMesh(meshId, fname)
    print()
    return meshId
