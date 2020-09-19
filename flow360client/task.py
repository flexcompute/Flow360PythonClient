import time

from flow360client.httputils import get2, put2, post2, delete2

def UpdateTask(item):
    return put2(f'solver/task/{item.itemId}', item)

def NewTask(item):
    return post2(f'solver/task', item)

def GetTask(itemId):
    return get2(f'solver/task/{itemId}')

def DeleteTask(itemId):
    return delete2(f'solver/task/{itemId}')

def ListTask(type):
    return get2(f'solver/{type}/tasks')

def WaitOnTask(taskId, timeout=86400, sleepSeconds=10):
    startTime = time.time()
    while time.time() - startTime < timeout:
        try:
            info = GetTask(taskId)
            if info['status'] in ['error', 'success']:
                return info['status']
        except Exception as e:
            print('Warning : {0}'.format(str(e)))

        time.sleep(sleepSeconds)




