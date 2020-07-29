import boto3 

class SessionProfile:
    def list_profiles(self):
        return boto3.session.Session().available_profiles