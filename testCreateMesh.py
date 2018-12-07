import boto3
import time
import requests
import json
from aws_requests_auth.aws_auth import AWSRequestsAuth

boto3.setup_default_session(region_name='us-east-1')

from warrant import Cognito
from warrant.aws_srp import AWSSRP


def getCredentials(username, password):

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

    return creds

def getAPIAuthentication(creds):
    auth = AWSRequestsAuth(aws_access_key=creds['Credentials']['AccessKeyId'],
                           aws_secret_access_key=creds['Credentials']['SecretKey'],
                           aws_token = creds['Credentials']['SessionToken'],
                           aws_host='zcvxbr69d2.execute-api.us-east-1.amazonaws.com',
                           aws_region='us-east-1',
                           aws_service='execute-api')
    return auth


creds = getCredentials('johnpmooreiv-at-gmail.com','LLEm4Crst')
auth = getAPIAuthentication(creds)

s3Client = boto3.client(
    's3',
    aws_access_key_id=creds['Credentials']['AccessKeyId'],
    aws_secret_access_key=creds['Credentials']['SecretKey'],
    aws_session_token=creds['Credentials']['SessionToken'],
)

flow360url = 'https://zcvxbr69d2.execute-api.us-east-1.amazonaws.com/beta'
url = '{0}/{1}'.format(flow360url, 'add-mesh')

body = {
      "name": "mymesh",
      "tags": ["test tag"],
      "endianness" : "little",
      "boundaries" : {"noSlipWalls" : [1]},
      "format": "aflr3"
    }



resp = requests.post(url, auth=auth, data=json.dumps(body))
print(resp.text)

resp.raise_for_status()
#print(dir(resp))
#print(resp.content)
#print(resp)
