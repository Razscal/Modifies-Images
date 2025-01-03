from urllib.parse import urlparse

if __name__ == "__main__":
	parsed_url= urlparse("s3://aws-bucket/OIP.jpg")
	bucket = parsed_url.netloc
	key = parsed_url.path.lstrip('/')
	print(bucket, key)