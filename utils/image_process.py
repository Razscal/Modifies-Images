from PIL import Image
import uuid
import time

async def main_process(img_id, origin_path, step):
	# Full pipe-line
	step+=1
	output_resize = f"files/{img_id}_{step}.png"
	print(output_resize)
	await resize_image(origin_path, output_resize)
	#Websocket notification
	step+=1
	output_resize = f"files/{img_id}_{step}.png"
	await resize_image(origin_path, output_resize)
	print(f"Processing {origin_path} with ID {img_id} at step {step}")

async def resize_image(input_path: str, output_path: str, width: int = 200, height: int = 200):
	time.sleep(5)
	with Image.open(input_path) as img:
		img = img.resize((width,height))
		img.save(output_path)
