import boto3


class Account:
    def __init__(self,new_account=False,access_key_id='',
                 secret_access_key='',
                 session_token='',
                 region='us-east-1',
                 profile="default"
                 ):
        session = boto3.Session(profile_name=profile)
        self.organization = session.client('organizations')
        print(access_key_id)
        if new_account:
            self.organization = session.client(
                                    'organizations',
                                    aws_access_key_id=access_key_id,
                                    aws_secret_access_key=secret_access_key,
                                    aws_session_token=session_token
                                    )
        paginator = self.organization.get_paginator('list_accounts')
        response_iterator = paginator.paginate(PaginationConfig={'MaxItems': 70,'PageSize': 5,})
        organizations=[]
        for i in response_iterator:
            for account in i['Accounts']:

                organizations.append({'id':account['Id'],
                                       'name':account['Name'],
                                       'email':account['Email'],
                                        })
        self.list_organizations=organizations
