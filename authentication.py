import boto3
import time
import requests
import getpass
import json
import hashlib
import os
import functools
from aws_requests_auth.aws_auth import AWSRequestsAuth

boto3.setup_default_session(region_name='us-east-1')

from warrant import Cognito
from warrant.aws_srp import AWSSRP

def getEmailPasswd():
    flow360dir = os.path.expanduser('~/.flow360')
    if os.path.exists('{0}/{1}'.format(flow360dir,'passwd')):
        with open(os.path.join(flow360dir,'passwd'),'r') as f:
            password = f.read()
    if os.path.exists('{0}/{1}'.format(flow360dir,'email')):
        with open(os.path.join(flow360dir,'email'),'r') as f:
            email = f.read()
    else:
        email = input('simulation.cloud email:')
        password = getpass.getpass()
        salt = '5ac0e45f46654d70bda109477f10c299'
        print(type(salt))
        print(type(password))
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
    return email.replace('@','-at-')


def getCredentials():
    username = email2username(email)
    u = Cognito('us-east-1_Csq1uNAO3','scepvluho5eeehv297pvdunk5',
                username=username,
                access_key='AKIAIOSFODNN7EXAMPLE',
                secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY')

    u.authenticate(password=password)

    client = boto3.client('cognito-identity',
                          region_name='us-east-1')

    login = {'cognito-idp.us-east-1.amazonaws.com/us-east-1_Csq1uNAO3' : u.id_token}

    resp =  client.get_id(AccountId='625554095313',
                          IdentityPoolId='us-east-1:68a3cf31-60fc-4def-8db2-4c3d48070756',
                          Logins=login)

    creds = client.get_credentials_for_identity(IdentityId=resp['IdentityId'],
                                                Logins=login)
    global tokenRefreshTime
    tokenRefreshTime = time.time()
    return creds

def getAPIAuthentication(creds):
    creds = getCredentials()

    auth = AWSRequestsAuth(aws_access_key=creds['Credentials']['AccessKeyId'],
                           aws_secret_access_key=creds['Credentials']['SecretKey'],
                           aws_token = creds['Credentials']['SessionToken'],
                           aws_host='nfbi4wgyr9.execute-api.us-east-1.amazonaws.com',
                           aws_region='us-east-1',
                           aws_service='execute-api')

    keys = requests.post('https://nfbi4wgyr9.execute-api.us-east-1.amazonaws.com/beta1/get-access', auth=auth).json()

    if keys['NewKeys']:
        sleepDur = 15
        print('Waiting {0}s for new keys to propagate...'.format(sleepDur))
        time.sleep(sleepDur)

    auth = AWSRequestsAuth(aws_access_key=keys['UserAccessKey'],
                           aws_secret_access_key=keys['UserSecretAccessKey'],
                           aws_host='dsxjn7ioqe.execute-api.us-gov-west-1.amazonaws.com',
                           aws_region='us-gov-west-1',
                           aws_service='execute-api')

    return auth, keys

auth, keys = getAPIAuthentication(getCredentials())

def refreshToken(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global creds
        global auth
        #auth = getAPIAuthentication(None)
        resp = func(*args, **kwargs)
        return resp
    return wrapper

