from helpers.aws_s3 import AWSS3
from transformers import pipeline
from PIL import Image
import io

aws_s3 = AWSS3()

if __name__ == "__main__":
	#aws_s3.upload_file('./testing.txt' ,'aws-bucket', 'testing.txt')
	file_content = aws_s3.get_file_content('s3://aws-bucket/OIP.jpg')
	img = Image.open(io.BytesIO(file_content))
	pipe = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)
	img = pipe(img)
	aws_s3.push_file_object(img, 'aws-bucket', 'xxx.png')