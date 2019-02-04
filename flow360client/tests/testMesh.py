import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mesh

mesh.user_id = 'AIDALXX5IIHVGTNCAOAP6'

resp = mesh.AddMesh('OM6_Wing_Tetra', [1], ['OM6'], 'aflr3', 'little')
print(resp)
meshId = resp['meshId']
print(meshId)

mesh.UploadMesh(meshId, 'data/wing_tetra.1.lb8.ugrid.gz')

resp = mesh.GetMeshInfo(meshId=meshId)
print(resp)

resp = mesh.ListMeshes()
print(resp)
