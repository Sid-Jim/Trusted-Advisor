from hermes.services.aws.support.trust_advisor import TrustAdvisor
from hermes.services.aws.organizations import accounts
from hermes.services.aws.sts import assume_role
from hermes.services.aws.ec2.regions import Region
from hermes.services.aws.session.session_profile import SessionProfile
from hermes.api.organization.csv import write_csv
from hermes.api.organization.csv.upload_csv_s3 import upload_file_and_delete

class TrustAdvisorReport:
    """
    Script for trust advisor report.
    """
    def __init__(self,region='us-east-1',master_role=''):
        self.headers_csv=['console','account','category','check','status','processed','flagged','suppressed','ignored','savings']
        self.csv = write_csv.CsvFile("trust_advisor",self.headers_csv,'infraestructure/')
        self.clients_account=accounts.Account()
        self.master_role=master_role

    def steps(self,tr_adv_obj,organization,profile):
        for i in tr_adv_obj:
            row = {
                'console':profile,
                'account':organization,
                'category':i['category'],
                'check':i['check'],
                'status':i['status'],
                'processed':i['processed'],
                'flagged':i['flagged'],
                'suppressed':i['suppressed'],
                'ignored':i['ignored'],
                'savings':i['savings']
            }
            self.csv.append_line(row)

    def __describe_trust_advisor_master(self,profile):
        tr_adr = TrustAdvisor(session_profile=profile)
        return tr_adr.describe_account_status()
    
    def __describe_trust_advisor_organization(self,aws_access_key_id,aws_secret_access_key,aws_session_token,profile):
        tr_adr = TrustAdvisor(new_account=True,
                                                access_key_id=aws_access_key_id,
                                                secret_access_key=aws_secret_access_key,
                                                session_token=aws_session_token,
                                                session_profile=profile)
        return tr_adr.describe_account_status()

    def execute_account(self,profile):
        ref_profile=profile
        if profile == 'default':
            ref_profile = 'Master' 
        print('-----\n'+ref_profile)
        tr_adv_obj=self.__describe_trust_advisor_master(profile=profile)
        self.steps(tr_adv_obj,'Master',ref_profile)
        
    def execute_organizations_account(self,profile):
        role = self.master_role
        ref_profile=profile
        if profile == 'default':
            ref_profile = 'Master'
        for organization in self.clients_account.list_organizations:
            organization_id = organization['id']
            organization_name = organization['name']
            try:
                credentials = assume_role.new_credentials(organization_id,role,profile_name=profile)
                print("-----\n"+organization_name)
                tr_adv_obj=self.__describe_trust_advisor_organization(credentials['AccessKeyId'],credentials['SecretAccessKey'],credentials['SessionToken'],profile=profile)   
                self.steps(tr_adv_obj,organization_name,ref_profile)
            except Exception as e:
                print("-----\nProblem with client: " + organization_name)
                print("Problem: "+ str(e))

    def execute(self):
        session_profile=SessionProfile()
        for profile in session_profile.list_profiles():
            self.clients_account=accounts.Account(profile=profile)
            self.execute_account(profile)
            self.execute_organizations_account(profile)
        upload_file_and_delete(self.csv.file_csv_name,self.csv.file_csv_name)