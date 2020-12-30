
from flow360client import mesh, NewCaseListWithPhase, Config

resp = mesh.AddMesh('cylinder.cgns', ["fluid/wall"], ['tag1'], 'cgns', '', Config.VERSION_CFD)
print(resp)
meshId = resp['meshId']
print(meshId)

mesh.UploadMesh(meshId, 'data/cylinder.cgns')

caseIds = NewCaseListWithPhase(meshId=meshId, config='data/cyclinder_case.json', caseName='test_case', tags=[],
            priority='high', parentId=None, phaseCount=1)

print(caseIds)