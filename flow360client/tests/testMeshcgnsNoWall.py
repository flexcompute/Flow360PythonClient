
from flow360client import mesh, NewMesh, NewCase

# meshId = NewMesh(fname='data/vortex_100.cgns', noSlipWalls=[], tags=['tag1'], fmat='cgns', endianness='', solverVersion='release-20.3.1')
# print(meshId)
#
# resp = mesh.ListMeshes()
# print(resp)

caseId = NewCase(meshId='45a9ddd3-d9f3-4b42-802e-d15eccb5653d', config='data/cyclinder_case.json', caseName='case2', tags=[],
            priority='high', parentId=None)

print(caseId)