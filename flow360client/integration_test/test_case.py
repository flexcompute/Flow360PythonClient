from unittest import TestCase

from flow360client import case

class TestFlow360Case(TestCase):
    def test_SubmitCase(self):
        resp = case.SubmitCase(
            "unittest_name"
            ,[1]
            ,"d62b5d68-ce74-4aab-8ed9-e6008c24cedb"
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
        print(resp)

    def test_DeleteCase(self):
        case.DeleteCase("58d025b3-b1c5-4b7c-be8e-aa91a7e4064e")

    def test_GetCaseInfo(self):
        caseInfo = case.GetCaseInfo("bc40fa12-a581-4cd9-8963-ed4f0b9088c2")
        print(caseInfo)

    def test_GetCaseInfo(self):
        caseInfo = case.GetCaseInfo("c51bb113-4cda-40f5-81c4-887cd8452126")
        print(caseInfo)

    def test_ListCases(self):
        cases = case.ListCases(include_deleted=False)
        print(cases)

    def test_GetCaseResidual(self):
        res = case.GetCaseResidual("45d15afd-00ee-47da-86e2-325c20846915")
        print(res)

    def test_GetCaseTotalForces(self):
        tf = case.GetCaseTotalForces("45d288e1-738b-4712-9e92-f15d903ba839")
        print(tf)

    def test_GetCaseSurfaceForces(self):
        sf = case.GetCaseSurfaceForces("45d15afd-00ee-47da-86e2-325c20846915",[])
        print(sf)

    def test_DownloadSurface(self):
        sf = case.DownloadSurfaceResults("45d15afd-00ee-47da-86e2-325c20846915")

    def test_DownloadVolumetricResults(self):
        sf = case.DownloadVolumetricResults("45d288e1-738b-4712-9e92-f15d903ba839")

    def test_DownloadSolver(self):
        sf = case.DownloadSolverOut("45d15afd-00ee-47da-86e2-325c20846915")

    def test_DownloadSolver(self):
        sf = case.DownloadResultsFile("45d288e1-738b-4712-9e92-f15d903ba839", "restart.tar.gz")
