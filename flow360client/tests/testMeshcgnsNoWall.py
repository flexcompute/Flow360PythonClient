
from flow360client import mesh, NewMesh

meshId = NewMesh(fname='data/vortex_100.cgns', noSlipWalls=[], tags=['tag1'], fmat='cgns', endianness='', solverVersion='release-20.3.1')
print(meshId)

resp = mesh.ListMeshes()
print(resp)

