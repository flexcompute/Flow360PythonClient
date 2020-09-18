from unittest import TestCase

from flow360client import mesh

from flow360client.mesh import ListMeshes, GetMeshInfo, getFileCompression, DeleteMesh


class TestMesh(TestCase):
    def test_GetMeshInfo(self):
        GetMeshInfo("bfa29e8f-5c9e-4777-8648-8c8f189c60a9")

    def test_DownloadMeshProc(self):
        mesh.DownloadMeshProc("aabbade3-1405-4b94-9fa2-c53dd4d64d8d")

    def test_ListMeshes(self):
        meshes = ListMeshes()
        print(meshes)

    def test_getFileCompression(self):
        compression = getFileCompression("abc.gz")
        print(compression)

    def test_DeleteMesh(self):
        resp = mesh.AddMesh('OM6_Wing_Tetra', [1], ['OM6'], 'aflr3', 'little', 'release-20.3.1')['data']
        print(resp)
        meshId = resp['meshId']
        print(meshId)
        DeleteMesh(meshId)
