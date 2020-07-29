import boto3
from operator import itemgetter

class TrustAdvisor:
    def __init__(self,new_account=False,access_key_id='',
                 secret_access_key='',
                 session_token='',
                 region='us-east-1',
                 session_profile="default"
                 ):
        self.region_ref=region
        session = boto3.Session(profile_name=session_profile)
        self.support = session.client('support', region_name=region)
        if new_account:
            self.support = session.client(
                                    'support',
                                    aws_access_key_id=access_key_id,
                                    aws_secret_access_key=secret_access_key,
                                    aws_session_token=session_token,
                                    region_name=region
                                    )
    def describe_account_status(self):
        ta_checks = self.support.describe_trusted_advisor_checks(language='en')
        #print(ta_checks)
        check_list=[{'name':c['name'],'category':c['category'],'id':c['id']} for c in ta_checks['checks']]
        data_list=[]
        for check in check_list:
            data={
                'category':'',
                'check':'',
                'status':'',
                'processed':'',
                'flagged':'',
                'suppressed':'',
                'ignored':'',
                'savings':''
            }
            new_check=self.support.describe_trusted_advisor_check_result(checkId=check['id'],language='en')
            data['category']=check['category']
            data['check']=check['name']
            data['status']=new_check['result']['status']
            if new_check['result']['status'] != "not_available":
                if 'resourcesSummary' in new_check['result']:
                    #print(new_check['result'])
                    data['processed']=new_check['result']['resourcesSummary']['resourcesProcessed']
                    data['flagged']=new_check['result']['resourcesSummary']['resourcesFlagged']
                    data['suppressed']=new_check['result']['resourcesSummary']['resourcesSuppressed']
                    data['ignored']=new_check['result']['resourcesSummary']['resourcesIgnored']
                #else:
                #    print("Not resources found")
                if 'categorySpecificSummary' in new_check['result']: 
                    if 'costOptimizing' in new_check['result']['categorySpecificSummary']:
                        data['savings']=new_check['result']['categorySpecificSummary']['costOptimizing']['estimatedMonthlySavings']
                    #else:
                    #    print("Not cost optimizations")
            #else:
            #    print("Not available")
            data_list.append(data)
            data_list = sorted(data_list, key=itemgetter('category'))
        return data_list