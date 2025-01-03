from transformers import pipeline
from urllib.parse import urlparse

input_path = '../local_storages/OIP.jpg'

if __name__ == "__main__":
	pipe = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)
	pillow_image = pipe(input_path)  # applies mask on input and returns a pillow image
	pillow_image.save(input_path.replace('.jpg', '.png'))






