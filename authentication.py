import boto3
import time
import requests
import getpass
import json
import os
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
        login = input('Do you want to keep logged in on this machine ([Y]es / [N]o)')
        if login == 'Y':
            try:
                os.mkdir(flow360dir)
            except OSError as e:
                pass

            with open(os.path.join(flow360dir,'passwd'),'w') as f:
                f.write(password)
            with open(os.path.join(flow360dir,'email'),'w') as f:
                f.write(email)
            
        elif login == 'N':
            os.mkdir(flow360dir)
        else:
            raise RuntimeError('Unknown keep logged in response {0}!'.format(login))
    return (email, password)

#email, password = getEmailPasswd()

with open(os.path.expanduser('~/.flow360/access_key'),'r') as f:
    access_key = f.read().strip()

with open(os.path.expanduser('~/.flow360/secret_access_key'),'r') as f:
    secret_access_key = f.read().strip()

#user_id = 'AIDALBZRC6BAHBQD3SRWU'

tokenRefreshTime = None
tokenDuration = 3500.
creds = None
auth = None

def email2username(email):
    return email.replace('@','-at-')

def refreshToken(func):
    def wrapper(*args, **kwargs):
        global creds
        global auth
        auth = getAPIAuthentication(None)
        resp = func(*args, **kwargs)
        return resp
    return wrapper

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
    auth = AWSRequestsAuth(aws_access_key=access_key,
                           aws_secret_access_key=secret_access_key,
                           aws_host='dsxjn7ioqe.execute-api.us-gov-west-1.amazonaws.com',
                           aws_region='us-gov-west-1',
                           aws_service='execute-api')

    return auth

auth = getAPIAuthentication(None)
