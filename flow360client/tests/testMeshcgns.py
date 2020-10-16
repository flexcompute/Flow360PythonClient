
from flow360client import mesh, NewCase

resp = mesh.AddMesh('cylinder.cgns', ["fluid/wall"], ['tag1'], 'cgns', '', 'release-20.3.1')
print(resp)
meshId = resp['meshId']
print(meshId)

mesh.UploadMesh(meshId, 'data/cylinder.cgns')

caseId = NewCase(meshId=meshId, config='data/cyclinder_case.json', caseName='case_stuck', tags=[],
            priority='high', parentId=None)

print(caseId)