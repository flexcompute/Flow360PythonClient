
# class Config:
#     S3_REGION="us-east-1"
#     CASE_BUCKET="flow360cases-v1"
#     MESH_BUCKET="flow360meshes-v1"
#     STUDIO_BUCKET="flow360-studio-v1"
#     WEB_API_ENDPONT="https://webapi-dev.flexcompute.com"
#
#     # auth info
#     auth = None
#     user = None
#
#     #other
#     auth_retry = 0
#     VERSION_CFD = 'beta-20.4.1'


class Config:
    S3_REGION="us-gov-west-1"
    CASE_BUCKET="flow360cases"
    MESH_BUCKET="flow360meshes"
    STUDIO_BUCKET="flow360studio"
    WEB_API_ENDPONT="https://webapi.flexcompute.com"

    # auth info
    auth = None
    user = None

    #other
    auth_retry = 0
    VERSION_CFD = 'release-20.3.2'
