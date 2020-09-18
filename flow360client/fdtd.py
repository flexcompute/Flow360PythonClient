import json
from .authentication import refreshToken
from .httputils import post2, delete2, get2
from .config import Config
auth = Config.auth
keys = Config.user
@refreshToken
def SubmitSimulation(jsno_file):
    data = ''
    with open(jsno_file, "r") as f:
        data = json.dumps(json.load(f))
    body = {
        "taskType": 'em',
        "status": 'wait',
        "taskParam": data,
    }
    url = f'solver/task'
    resp = post2(url, data=body)
    return resp

@refreshToken
def DeleteSimulation(fdtdId):

    url = f'solver/task/{fdtdId}'
    resp = delete2(url)
    return resp

@refreshToken
def GetSimulationInfo(fdtdId):

    url = f'solver/task/{fdtdId}'

    resp = get2(url)
    return resp

@refreshToken
def ListSimulations():

    url = f'solver/em/tasks'

    resp = get2(url)
    resp = list(filter(lambda i : i['status'] != 'deleted', resp))
    return resp

@refreshToken
def GetSimulationResult(fdtdId):

    url = f'solver/task/{fdtdId}/visualize'
    resp = get2(url)
    return resp
