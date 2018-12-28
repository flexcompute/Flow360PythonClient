import time
from mesh import UploadMesh, AddMesh, ListMeshes, DeleteMesh, GetMeshInfo


resp = AddMesh('hlcrm0',[1], ['alpha 8', 'beta 0'], 'aflr3', 'big')
print(resp)
meshId = resp['meshId']
print(meshId)

#meshId = 'fc89683b-bd80-4f68-b9d1-799612d6268c'
#meshId = '5a7327de-1e41-4ccf-a9ec-dbd7d18c522b'
#meshId = 'b10f53fb-3e08-4c24-a1c6-26090b4c4281'

#UploadMesh(meshId, 'wing.ugrid')
#UploadMesh(meshId, 'mesh.py')
#time.sleep(5)
#time.sleep(10)

#resp = GetMeshInfo(meshId=meshId)
#print(resp)

#time.sleep(10)
#resp = ListMeshes()
#print(resp)

#DeleteMesh(meshId)

