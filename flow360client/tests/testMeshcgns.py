
from flow360client import mesh, NewCase, NewCaseListWithPhase

resp = mesh.AddMesh('cylinder.cgns', ["fluid/wall"], ['tag1'], 'cgns', '', None)
print(resp)
meshId = resp['meshId']
print(meshId)

mesh.UploadMesh(meshId, 'data/cylinder.cgns')

caseIds = NewCaseListWithPhase(meshId=meshId, config='data/cyclinder_case.json', caseName='case_stuck', tags=[],
            priority='high', parentId=None, phaseCount=3)

print(caseIds)