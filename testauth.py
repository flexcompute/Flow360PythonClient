import boto3
import time
boto3.setup_default_session(region_name='us-east-1')

from warrant import Cognito
from warrant.aws_srp import AWSSRP


#aws = AWSSRP(username='johnpmooreiv-at-gmail.com', password='LLEm4Crst', pool_id='us-east-1_Csq1uNAO3', client_id='scepvluho5eeehv297pvdunk5', client=client2)
#tokens = aws.authenticate_user()
#print(tokens)

u = Cognito('us-east-1_Csq1uNAO3','scepvluho5eeehv297pvdunk5',
            username='johnpmooreiv-at-gmail.com',
            access_key='AKIAIOSFODNN7EXAMPLE',
            secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY')

u.authenticate(password='LLEm4Crst')

client = boto3.client('cognito-identity',region_name='us-east-1')

#client2 = boto3.client('cognito-idp',region_name='us-east-1')

#login = {'cognito-identity.amazonaws.com' : u.id_token}
login = {'cognito-idp.us-east-1.amazonaws.com/us-east-1_Csq1uNAO3' : u.id_token}

#creds = client.get_credentials_for_identity(IdentityId="u, login=login)

print(dir(u))
print(u.id_token)
print(u.access_token)
print(u.token_type)
#print(u.get_key())
#print(u.token)
#response = client.get_credentials_for_identity(IdentityId="us-east-1:9d8ae0c8-0583-45f0-9ea2-bb56471c1103", Logins={'cognito-identity.amazonaws.com' : u.access_token})

resp =  client.get_id(AccountId='625554095313',IdentityPoolId='us-east-1:68a3cf31-60fc-4def-8db2-4c3d48070756', Logins=login)
print(resp)
#quit()
creds = client.get_credentials_for_identity(IdentityId=resp['IdentityId'], Logins=login)


print(creds)

s3Client = boto3.client(
        's3',
        aws_access_key_id=creds['Credentials']['AccessKeyId'],
        aws_secret_access_key=creds['Credentials']['SecretKey'],
        aws_session_token=creds['Credentials']['SessionToken'],
    )
print('cognito/flow360-app/{0}'.format(resp['IdentityId']))

s3Client.put_object(Bucket='flow360data',
                    Body=b'abcd',
                    Key='users/{0}/test.txt'.format(resp['IdentityId']))

get = s3Client.get_object(Bucket='flow360data',
                          Key='users/{0}/test.txt'.format(resp['IdentityId']))
print(get['Body'].read())

#lb = s3Client.list_objects(Bucket='flow360data',Prefix='users/{0}/'.format(resp['IdentityId']))
#print(lb)

#s3Client.list_objects(Bucket='flow360data')

#user = u.get_users(attr_map={"email":"email"})
#print(user[3])
#user[3].delete()
#user = u.get_users()
#firstUser = user[3]
#user[3].delete()

#print(dir(firstUser))
#print(user)

#print(dir(u))
#print(u.id_token)
#print(u.check_token())
