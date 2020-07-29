import boto3

def new_credentials(client_id,role,profile_name="default"):
        session = boto3.Session(profile_name=profile_name)
        sts_client =  session.client('sts')
        assumed_role_object=sts_client.assume_role(
        RoleArn='arn:aws:iam::'+client_id+':role/'+role,
        RoleSessionName='AssumeRoleSession',
        )
        credentials=assumed_role_object['Credentials']
        return credentials