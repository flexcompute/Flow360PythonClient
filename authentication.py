import boto3
import time
import requests
import json
from aws_requests_auth.aws_auth import AWSRequestsAuth

boto3.setup_default_session(region_name='us-east-1')

from warrant import Cognito
from warrant.aws_srp import AWSSRP

email = ''
password = ''

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
        if tokenRefreshTime is None:
            creds = getCredentials()
            auth = getAPIAuthentication(creds)
        elif time.time() - tokenRefreshTime > tokenDuration:
            print('refreshing tokens...')
            creds = getCredentials()
            auth = getAPIAuthentication(creds)
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
    auth = AWSRequestsAuth(aws_access_key=creds['Credentials']['AccessKeyId'],
                           aws_secret_access_key=creds['Credentials']['SecretKey'],
                           aws_token = creds['Credentials']['SessionToken'],
                           aws_host='zcvxbr69d2.execute-api.us-east-1.amazonaws.com',
                           aws_region='us-east-1',
                           aws_service='execute-api')
    return auth

creds = getCredentials()
auth = getAPIAuthentication(creds)
