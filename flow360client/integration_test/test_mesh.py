import json
from unittest import TestCase

from flow360client import mesh, NewMeshWithTransform

from flow360client.mesh import ListMeshes, GetMeshInfo, getFileCompression, DeleteMesh


class TestMesh(TestCase):
    def test_GetMeshInfo(self):
        GetMeshInfo("bfa29e8f-5c9e-4777-8648-8c8f189c60a9")

    def test_DownloadMeshProc(self):
        mesh.DownloadMeshProc("bfa29e8f-5c9e-4777-8648-8c8f189c60a9")

    def test_ListMeshes(self):
        meshes = ListMeshes()
        print(meshes)

    def test_getFileCompression(self):
        compression = getFileCompression("abc.gz")
        print(compression)

    def test_DeleteMesh(self):
        resp = mesh.AddMesh('OM6_Wing_Tetra', [1], ['OM6'], 'aflr3', 'little', 'release-20.3.2')
        print(resp)
        meshId = resp['meshId']
        print(meshId)
        DeleteMesh(meshId)

    def test_NewMeshTransform(self):
        NewMeshWithTransform('data/transform/all.json', 'test')

    def test_AddMeshMeshWithJson(self):
        with open('data/wing_tetra.1.json') as json_file:
            resp = mesh.AddMeshWithJson('OM6_Wing_Tetra', json.load(json_file), ['OM6'], 'aflr3', 'little', 'release-20.3.2')
            print(resp)
            meshId = resp['meshId']
            print(meshId)
