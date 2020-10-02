
from flow360client import mesh, NewMesh, NewCase

meshId = NewMesh(fname='data/vortex_100.cgns', noSlipWalls=[], tags=['tag1'], fmat='cgns', endianness='', solverVersion='release-20.3.2')
print(meshId)

resp = mesh.ListMeshes()
print(resp)
caseId = NewCase(meshId=meshId, config='data/cyclinder_case.json', caseName='case2', tags=[],
            priority='high', parentId=None)

print(caseId)