from PIL import Image

async def main_process(input_path, output_path):
	await resize_image(input_path, output_path)
	print("Done resize image")

async def resize_image(input_file_path: str, output_file_path: str, width: int = 200, height: int = 200):
	with Image.open(input_file_path) as img:
		img = img.resize((width,height))
		img.save(output_file_path)