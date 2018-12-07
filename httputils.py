import requests
import urllib

def handle_response(func):
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        #print(resp.text)
        if resp.status_code != 200:
            print(resp.text)
            resp.raise_for_status()
        try:
            jsn = resp.json()
        except Exception as e:
            print('Could not json decode response : {0}!'.format(resp.text))
            raise
        return jsn
    return wrapper

@handle_response
def post(url, data, auth=None, headers=None):
    return requests.post(url, auth=auth, data=data)

@handle_response
def get(url, params=None, auth=None, headers=None):
    if params is None:
        queryUrl = url
    else:
        queryUrl = '{0}?{1}'.format(url, urllib.parse.urlencode(params))
    return requests.get(queryUrl, auth=auth)

@handle_response
def delete(url, params=None, auth=None, headers=None):
    if params is None:
        queryUrl = url
    else:
        queryUrl = '{0}?{1}'.format(url, urllib.parse.urlencode(params))
    return requests.delete(queryUrl, auth=auth)

