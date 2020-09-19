import uuid
from unittest import TestCase

from flow360client import UploadStudioItem


class TestStudio(TestCase):
    def test_UploadStudioItem(self):
        UploadStudioItem(uuid.uuid1(), )

    def test_UpdateStudioObject(self):
        self.fail()

    def test_NewStudioObject(self):
        self.fail()

    def test_GetStudioObject(self):
        self.fail()

    def test_DeleteStudioObject(self):
        self.fail()

    def test_CopyResourceToMesh(self):
        self.fail()
