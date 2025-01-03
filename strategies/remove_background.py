from typing import Dict

import torch
from fastapi.responses import FileResponse
from transformers import pipeline
from abstracts.image_actions import ImageActions
from PIL import Image
import io
from helpers.aws_s3 import AWSS3
from urllib.parse import urlparse

class RemoveBackground(ImageActions):
	def __init__(self, s3 : AWSS3):
		self.s3 = s3

	def action(self, s3_url: str, bucket_name: str) -> Dict[str, str] :
		try:
			file_name = urlparse(s3_url).path.lstrip('/')
			file_content = self.s3.get_file_content(s3_url)

			pil_img = Image.open(io.BytesIO(file_content))
			pipe = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True, device=self.device)
			pillow_image = pipe(pil_img)

			self.s3.push_file_object(pillow_image, bucket_name ,file_name)

			return {
				"message" : f"remove background file and push to {s3_url}"
			}
		except Exception as e:
			raise Exception(e)

if __name__ == '__main__':
	rmbg = RemoveBackground(AWSS3())
	rmbg.action('s3://aws-bucket/OIP.jpg', "aws-bucket")
