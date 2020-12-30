
from flow360client import mesh, NewMesh, NewCase, Config

meshId = NewMesh(fname='data/cylinder.cgns', noSlipWalls=["fluid/wall"], tags=['tag1'], fmat='cgns', endianness='', solverVersion=Config.VERSION_CFD)
print(meshId)

resp = mesh.ListMeshes()
print(resp)
caseId = NewCase(meshId=meshId, config='data/cyclinder_case.json', caseName='cyclinder_case_2', tags=[],
            priority='high', parentId=None)

print(caseId)