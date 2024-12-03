from PIL import Image
import uuid

async def main_process(input_path, output_path):
	# Full pipe-line
	output_resize = f"files/{uuid.uuid4()}_1.png"
	await resize_image(input_path, output_resize)
	print("Done resize image")

async def resize_image(input_file_path: str, output_file_path: str, width: int = 200, height: int = 200):
	with Image.open(input_file_path) as img:
		img = img.resize((width,height))
		img.save(output_file_path)