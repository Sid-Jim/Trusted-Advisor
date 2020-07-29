import boto3

class Region:
    def __init__(self,new_account=False,access_key_id='',
                 secret_access_key='',
                 session_token='',
                 region='us-east-1'
                 ):
        self.ec2 = boto3.client('ec2')
        if new_account:
            self.ec2 = boto3.client(
                                    'ec2',
                                    aws_access_key_id=access_key_id,
                                    aws_secret_access_key=secret_access_key,
                                    aws_session_token=session_token
                                    )
        self.describe = [region['RegionName'] for region in self.ec2.describe_regions()['Regions']]