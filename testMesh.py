from mesh import UploadMesh, AddMesh, ListMeshes, DeleteMesh, GetMeshInfo


resp = AddMesh('hlcrm0',[1], ['alpha 8', 'beta 0'], 'aflr3', 'big')
meshId = resp['meshId']
print(meshId)

UploadMesh(meshId, '/home/john/fun3dcases/HLCRM/HLCRM_FullGap_Coarse.b8.ugrid')

resp = GetMeshInfo(meshId=meshId)
print(resp)

resp = ListMeshes(name='hlcrm0')
print(resp)

#DeleteMesh(meshId)

