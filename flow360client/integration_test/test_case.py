from unittest import TestCase

from flow360client import case

class TestFlow360Case(TestCase):
    def test_SubmitCase(self):
        case.SubmitCase(
            "unittest_name"
            ,[1]
            ,"bfa29e8f-5c9e-4777-8648-8c8f189c60a9"
            ,"high"
            ,'''
            {
              "geometry": {
                "meshName": "wing_tetra.1.lb8.ugrid",
                "endianness": "big",
                "refArea": 297360,
                "momentCenter": [
                  1325.9,
                  468.75,
                  177.95
                ],
                "momentLength": [
                  275.8,
                  275.8,
                  275.8
                ]
              },
              "runControl": {
                "restart": false,
                "firstOrderIterations": -1
              }
            }
            '''
        )

    def test_DeleteCase(self):
        case.DeleteCase("58d025b3-b1c5-4b7c-be8e-aa91a7e4064e")

    def test_GetCaseInfo(self):
        caseInfo = case.GetCaseInfo("bc40fa12-a581-4cd9-8963-ed4f0b9088c2")
        print(caseInfo)

    def test_GetCaseInfo(self):
        caseInfo = case.GetCaseInfo("bc40fa12-a581-4cd9-8963-ed4f0b9088c2")
        print(caseInfo)

    def test_ListCases(self):
        cases = case.ListCases(include_deleted=False)
        print(cases)

    def test_GetCaseResidual(self):
        res = case.GetCaseResidual("bc40fa12-a581-4cd9-8963-ed4f0b9088c2")
        print(res)

    def test_GetCaseTotalForces(self):
        tf = case.GetCaseTotalForces("bc40fa12-a581-4cd9-8963-ed4f0b9088c2")
        print(tf)

    def test_GetCaseSurfaceForces(self):
        sf = case.GetCaseSurfaceForces("a1a7103c-21ff-49ff-8328-dc85d9bc62d3",[])
        print(sf)

    def test_DownloadSurface(self):
        sf = case.DownloadSurfaceResults("e49d38b5-e39b-4ac9-85aa-5466d8cef516")

    def test_DownloadSolver(self):
        sf = case.DownloadSolverOut("b06f21b4-481a-4804-afd4-3c4429c273ce")
