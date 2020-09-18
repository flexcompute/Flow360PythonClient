
from flow360client import mesh, NewCase

resp = mesh.AddMesh('cylinder.cgns', ["fluid/wall"], ['tag1'], 'cgns', '', 'release-20.3.2')
print(resp)
meshId = resp['meshId']
print(meshId)

mesh.UploadMesh(meshId, 'data/cylinder.cgns')
resp = mesh.GetMeshInfo(meshId=meshId)
print(resp)

resp = mesh.ListMeshes()
print(resp)

caseId = NewCase(meshId=meshId, config='data/cyclinder_case.json', caseName='case2', tags=["flow360-no-cleanup"],
            priority='high', parentId=None)

print(caseId)