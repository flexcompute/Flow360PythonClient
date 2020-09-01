
from flow360client import mesh, NewCase

resp = mesh.AddMesh('cylinder.cgns', ["fluid/wall"], ['tag1'], 'cgns', '', 'release-20.3.1')
print(resp)
meshId = resp['meshId']
print(meshId)

mesh.UploadMesh(meshId, 'data/cylinder.cgns')
resp = mesh.GetMeshInfo(meshId=meshId)
print(resp)

resp = mesh.ListMeshes()
print(resp)

meshId = "1aee3ed4-1683-43de-a734-f50c8cdd15b3"
caseId = NewCase(meshId=meshId, config='data/cyclinder_case.json', caseName='case2', tags=[],
            priority='high', parentId=None)

print(caseId)