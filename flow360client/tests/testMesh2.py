from flow360client import mesh

resp = mesh.AddMesh2(name='om6_test',
                     mesh_json='data/om6wing/Flow360Mesh.json',
                     tags=['ownFlow360Mesh.json'],
                     fmat='aflr3',
                     endianness='little',
                     solver_version='release-20.3.2')

meshId = resp['meshId']
print(meshId)
mesh.UploadMesh(meshId, '/data/om6wing/wing_tetra.1.lb8.ugrid')
