
from flow360client import mesh

resp = mesh.AddMesh('vortex_100.cgns', [], ['tag1'], 'cgns', '', 'release-20.3.1')
print(resp)
meshId = resp['meshId']
print(meshId)

mesh.UploadMesh(meshId, 'data/vortex_100.cgns')
resp = mesh.GetMeshInfo(meshId=meshId)
print(resp)

resp = mesh.ListMeshes()
print(resp)

