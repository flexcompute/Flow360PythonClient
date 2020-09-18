from unittest import TestCase

from flow360client import case, fdtd


class TestFlow360FDTD(TestCase):
    def test_SubmitSimulation(self):
        resp = fdtd.SubmitSimulation('./data/fdtd/fdtd3d.json')
        print(resp)

    def test_DeleteSimulation(self):
        fdtd.DeleteSimulation("e2ede678-9b5e-473d-b28d-9537f6a893af")

    def test_GetSimulationInfo(self):
        fdtdInfo = fdtd.GetSimulationInfo("e2ede678-9b5e-473d-b28d-9537f6a893af")
        print(fdtdInfo)

    def test_GetSimulationResult(self):
        fdtdRes = fdtd.GetSimulationResult("e2ede678-9b5e-473d-b28d-9537f6a893af")
        print(fdtdRes)

