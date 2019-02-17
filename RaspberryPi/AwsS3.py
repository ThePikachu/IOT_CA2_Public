import boto3
import botocore
import sys
import os
sys.path.append(os.path.abspath('..'))
from Shared.Configs import Config

class AwsS3:
    def __init__(self):
        self.s3 = boto3.resource('s3',
        aws_access_key_id=Config.aws_S3_access_key,
        aws_secret_access_key=Config.aws_S3_secret_key)

    def Upload(self,file_path, file_name):
        self.s3.Object(Config.aws_S3_bucket, file_name).put(Body=open(file_path, 'rb'))
        print("File uploaded")
