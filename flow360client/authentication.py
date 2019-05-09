import boto3
import getpass
from flow360client.httputils import get, flow360url
import hashlib
import os
import functools
from aws_requests_auth.aws_auth import AWSRequestsAuth

boto3.setup_default_session(region_name='us-east-1')


def getEmailPasswd():
    flow360dir = os.path.expanduser('~/.flow360')
    if os.path.exists('{0}/{1}'.format(flow360dir,'passwd')):
        with open(os.path.join(flow360dir,'passwd'),'r') as f:
            password = f.read()
    if os.path.exists('{0}/{1}'.format(flow360dir,'email')):
        with open(os.path.join(flow360dir,'email'),'r') as f:
            email = f.read()
    else:
        email = input('enter your email registered at flexcompute:')
        password = getpass.getpass()
        salt = '5ac0e45f46654d70bda109477f10c299'
        password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        login = input('Do you want to keep logged in on this machine ([Y]es / [N]o)')
        if login == 'Y':
            os.makedirs(flow360dir, exist_ok=True)
            with open(os.path.join(flow360dir,'passwd'),'w') as f:
                f.write(password)
            with open(os.path.join(flow360dir,'email'),'w') as f:
                f.write(email)
        elif login == 'N':
            os.makedirs(flow360dir, exist_ok=True)
        else:
            raise RuntimeError('Unknown keep logged in response {0}!'.format(login))
    return (email, password)

email, password = getEmailPasswd()

tokenRefreshTime = None
tokenDuration = 3500.


def email2username(email):
    return email.replace('@', '-at-')


def getAPIAuthentication():
    url = '{0}/{1}'.format(flow360url, 'get-access')
    auth = (email, password)

    keys = get(url, auth=auth)

    auth = AWSRequestsAuth(aws_access_key=keys['UserAccessKey'],
                           aws_secret_access_key=keys['UserSecretAccessKey'],
                           aws_host='dsxjn7ioqe.execute-api.us-gov-west-1.amazonaws.com',
                           aws_region='us-gov-west-1',
                           aws_service='execute-api')

    return auth, keys


auth, keys = getAPIAuthentication()


def refreshToken(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global creds
        global auth
        resp = func(*args, **kwargs)
        return resp
    return wrapper

