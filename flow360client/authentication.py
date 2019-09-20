import boto3
import getpass
from flow360client.httputils import get, flow360url
import hashlib
import os
import functools
from aws_requests_auth.aws_auth import AWSRequestsAuth

boto3.setup_default_session(region_name='us-east-1')

def email2username(email):
    return email.replace('@', '-at-')

def getAPIAuthentication(email, password):
    url = '{0}/{1}'.format(flow360url, 'get-access')
    auth = (email, password)

    keys = get(url, auth=auth)

    auth = AWSRequestsAuth(aws_access_key=keys['UserAccessKey'],
                           aws_secret_access_key=keys['UserSecretAccessKey'],
                           aws_host='dsxjn7ioqe.execute-api.us-gov-west-1.amazonaws.com',
                           aws_region='us-gov-west-1',
                           aws_service='execute-api')

    return auth, keys

def getEmailPasswdAuthKey():
    flow360dir = os.path.expanduser('~/.flow360')
    if os.path.exists('{0}/{1}'.format(flow360dir,'email')) and \
       os.path.exists('{0}/{1}'.format(flow360dir,'passwd')):
        with open(os.path.join(flow360dir,'email'),'r') as f:
            email = f.read()
        with open(os.path.join(flow360dir,'passwd'),'r') as f:
            password = f.read()
        try:
            auth, key = getAPIAuthentication(email, password)
            return (email, password, auth, key)
        except:
            print('Error: Failed to log in with existing user:', email)
            print()
            pass
    while True:
        email = input('enter your email registered at flexcompute: ')
        password = getpass.getpass()
        salt = '5ac0e45f46654d70bda109477f10c299'
        password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        try:
            auth, key = getAPIAuthentication(email, password)
            break
        except:
            print('Error: Failed to log in with new username and password.')
            print()
            pass
    while True:
        login = input('Do you want to keep logged in on this machine ([Y]es / [N]o) ')
        if login == 'Y' or login == 'y':
            os.makedirs(flow360dir, exist_ok=True)
            with open(os.path.join(flow360dir,'passwd'),'w') as f:
                f.write(password)
            with open(os.path.join(flow360dir,'email'),'w') as f:
                f.write(email)
            break
        elif login == 'N' or login == 'n':
            os.makedirs(flow360dir, exist_ok=True)
            break
        else:
            print('    Unknown response: {0}\n'.format(login))
    return (email, password, auth, key)


def refreshToken(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global creds
        global auth
        resp = func(*args, **kwargs)
        return resp
    return wrapper

tokenRefreshTime = None
tokenDuration = 3500.

email, password, auth, keys = getEmailPasswdAuthKey()
