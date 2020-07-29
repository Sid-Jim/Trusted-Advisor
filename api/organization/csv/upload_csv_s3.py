from hermes.services.aws.s3.buckets import Bucket
from hermes.config import BaseConfig
import os
#from dotenv import load_dotenv

btk_config=BaseConfig()
BUCKET_AWS_ACCESS_KEY_ID=btk_config.BUCKET_AWS_ACCESS_KEY_ID #os.environ.get('BUCKET_AWS_ACCESS_KEY_ID')
BUCKET_AWS_SECRET_ACCESS_KEY=btk_config.BUCKET_AWS_SECRET_ACCESS_KEY  #os.environ.get('BUCKET_AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = btk_config.BUCKET_NAME#os.environ.get('BUCKET_NAME')
#load_dotenv(os.path.join('.', '.env'))

def upload_file_and_delete(name_file,path):
    s3_bucket = Bucket(new_account=True,
                       access_key_id=BUCKET_AWS_ACCESS_KEY_ID,
                       secret_access_key=BUCKET_AWS_SECRET_ACCESS_KEY
                 )
    key_file=name_file.split("/")[-3]+"/"+name_file.split("/")[-2]+"/"+name_file.split("/")[-1]             
    s3_bucket.upload_file_bucket(path, 'inbest-reports', key_file)
    
    os.remove(name_file)
    