
from flow360client import NewCase

meshId = "eb352355-1722-4cc8-bee6-99923165f4bd"
caseId = NewCase(meshId=meshId, config='data/cyclinder_case.json', caseName='case2', tags=["flow360-no-cleanup"],
            priority='high', parentId=None)

print(caseId)