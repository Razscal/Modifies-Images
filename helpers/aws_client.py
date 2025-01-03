import boto3
from botocore.client import BaseClient

class AWSClient:
	def __init__(self, service: str, endpoint_url:str, access_key: str, secret_key: str, region: str):
		self.service = service
		self.endpoint_url = endpoint_url
		self.access_key = access_key
		self.secret_key = secret_key
		self.region = region

	def get_client(self) -> BaseClient:
		return boto3.client(self.service, endpoint_url=self.endpoint_url, aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key, region_name=self.region)

aws_client = AWSClient(service='s3',
                       region='us-east-1',
                       endpoint_url='http://localhost.localstack.cloud:4566',
                       access_key="",
                       secret_key="").get_client()