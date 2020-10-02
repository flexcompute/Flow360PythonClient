
from flow360client import mesh, NewCase

resp = mesh.AddMesh('cylinder.cgns', ["fluid/wall"], ['tag1'], 'cgns', '', 'release-20.3.2')
print(resp)
meshId = resp['meshId']
print(meshId)

mesh.UploadMesh(meshId, '/Users/leizheng/vcs/github/flow360/Flow360PythonClient/flow360client/tests/data/cylinder.cgns')

caseId = NewCase(meshId=meshId, config='data/cyclinder_case.json', caseName='case2', tags=[],
            priority='high', parentId=None)

print(caseId)