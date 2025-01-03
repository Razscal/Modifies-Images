from botocore.client import BaseClient
from botocore.exceptions import ClientError, NoCredentialsError
from helpers.aws_client import aws_client
from urllib.parse import urlparse
from typing import Dict
from PIL import Image
import io

class AWSS3:
	def __init__(self) -> None:
		self.client : BaseClient = aws_client

	def upload_file(self, file_name: str, bucket: str, key: str) -> None:
		try:
			self.client.upload_file(file_name, bucket, key)
		except ClientError as e:
			print(f"Client error {e}")
		except NoCredentialsError as e:
			print(f"No client error: {e}")

	def pull_file(self, s3_url: str, local_path: str) -> Dict[str, str]:
		parsed_url = urlparse(s3_url)
		bucket = parsed_url.netloc
		key = parsed_url.path.lstrip('/')

		self.client.download_file(bucket, key, local_path)
		return {
			"message" : f"file {key} is downloaded from bucket {bucket}",
		}

	def get_file_content(self, s3_url:str):
		try:
			parsed_url = urlparse(s3_url)
			bucket = parsed_url.netloc
			key = parsed_url.path.lstrip('/')

			response = self.client.get_object(Bucket=bucket, Key=key)

			file_content = response['Body'].read()
		except ClientError as e:
			print(f"Client error {e}")
		except NoCredentialsError as e:
			print(f"No client error: {e}")

		return file_content

	def push_file_object(self, image: Image, bucket_name: str, key: str):
		try:
			image_stream = io.BytesIO()
			image.save(image_stream, format='PNG')
			image_stream.seek(0)

			self.client.upload_fileobj(image_stream, bucket_name, key, ExtraArgs={"ContentType": "image/png"})
			return {"message" : f"upload file object successfully to bucket {bucket_name} and key {key}"}
		except ClientError as e:
			print(f"Client error {e}")
		except NoCredentialsError as e:
			print(f"No client error: {e}")
