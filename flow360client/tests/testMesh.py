
from flow360client import mesh, NewCase

resp = mesh.AddMesh('OM6_Wing_Tetra', "[2]", ['OM6'], 'aflr3', 'little', 'release-20.3.2')
print(resp)
meshId = resp['meshId']
print(meshId)

mesh.UploadMesh(meshId, 'data/wing_tetra.1.lb8.ugrid.gz')

resp = mesh.GetMeshInfo(meshId=meshId)
print(resp)

resp = mesh.ListMeshes()
print(resp)

caseId = NewCase(meshId=meshId, config='data/wing_tetra.1.json', caseName='case2_unittest', tags=[],
            priority='high', parentId=None)