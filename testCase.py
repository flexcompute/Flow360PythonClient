import time
from case import *


resp = SubmitCase('test0',['first tag', 'second tag'], 'b10f53fb-3e08-4c24-a1c6-26090b4c4281', 'low', 'Flow360_8.json')
#resp = ListCases()
#resp = GetCaseResidual('f5f98ad8-09b4-453a-9585-d656b2197e0c')
#resp = GetCaseTotalForces('f5f98ad8-09b4-453a-9585-d656b2197e0c')
#resp = GetCaseSurfaceForces('f5f98ad8-09b4-453a-9585-d656b2197e0c', [0,1,2,8])


#resp = GetCaseInfo('f5f98ad8-09b4-453a-9585-d656b2197e0c')
#DeleteCase('f5f98ad8-09b4-453a-9585-d656b2197e0c')
#resp = PauseResumeCase('f5f98ad8-09b4-453a-9585-d656b2197e0c', 'pause')
print(resp)

#print(resp)

#caseId = resp['caseId']
#print(caseId)
