from PIL import Image
import uuid
import time
import cv2
import numpy as np
from sqlalchemy.orm import defer
from transformers import pipeline

from GFPGAN.gfpgan import GFPGANer
import os
from basicsr.utils import imwrite


async def main_process(img_id, origin_path, step, positive, negative):
	# Step 1 #SUPIR

	# Step 2 #Desaturate
	step += 1
	output_path = f"files/{img_id}_{step}.png"
	input_path =  image_desaturate(origin_path, output_path)


	# Step 3 #GFPGAN
	step+=1
	output_path = f"files/{img_id}_{step}.png"
	input_path =  gfpgan(input_path, output_path)

	#Step 4 #BRIAA
	step += 1
	output_path = f"files/{img_id}_{step}.png"
	input_path =  briaa(input_path, output_path)

	#Step 5 #ControlNet, positive, negative prompt

	#Step 6 #Output


def image_desaturate(image_path, output_path, factor=1.0, method="luminance"):
	image = cv2.imread(image_path)
	if image is None:
		raise ValueError("Không thể đọc ảnh đầu vào!")

	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# Luminance theo Rec.709 (phương pháp phổ biến)
	if method == "luminance":
		weights = np.array([0.2126, 0.7152, 0.0722])  # Rec.709
	else:
		raise ValueError("Phương pháp không được hỗ trợ!")

	# Tính toán luminance
	grayscale = np.dot(image[..., :3], weights)

	# Áp dụng desaturation với factor
	desaturated = (1 - factor) * image + factor * grayscale[..., None]
	desaturated = np.clip(desaturated, 0, 255).astype(np.uint8)

	# Lưu ảnh kết quả
	desaturated = cv2.cvtColor(desaturated, cv2.COLOR_RGB2BGR)
	cv2.imwrite(output_path, desaturated)
	print(f"Đã lưu ảnh desaturated tại: {output_path}")
	return output_path

def gfpgan(input_path: str, output_path: str):
	# ------------------------ input & output ------------------------
	if not os.path.isfile(input_path):
		raise ValueError(f'The input path {input_path} is not a valid file.')

	# ------------------------ set up GFPGAN restorer for model 1.4 ------------------------
	arch = 'clean'
	channel_multiplier = 2
	model_name = 'GFPGANv1.4'
	url = 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth'

	# determine model paths
	model_path = os.path.join('experiments/pretrained_models', model_name + '.pth')
	if not os.path.isfile(model_path):
		model_path = os.path.join('gfpgan/weights', model_name + '.pth')
	if not os.path.isfile(model_path):
		# download pre-trained models from url
		model_path = url

	restorer = GFPGANer(
		model_path=model_path,
		upscale=3,
		arch=arch,
		channel_multiplier=channel_multiplier,
		bg_upsampler=None)  # No background upsampler

	# ------------------------ restore ------------------------
	img_name = os.path.basename(input_path)
	print(f'Processing {img_name} ...')
	input_img = cv2.imread(input_path, cv2.IMREAD_COLOR)

	# restore faces and background if necessary
	cropped_faces, restored_faces, restored_img = restorer.enhance(
		input_img,
		has_aligned=False,  # Assuming input is not aligned
		only_center_face=False,
		paste_back=True,
		weight=0.5)  # Default weight

	# Save restored image
	if restored_img is not None:
		save_restore_path = output_path
		imwrite(restored_img, save_restore_path)
		print(f"{save_restore_path} is saved")
	return output_path

def briaa(input_path: str, output_path:str):
	image_path = input_path
	pipe = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)
	pillow_mask = pipe(image_path, return_mask=True)  # outputs a pillow mask
	pillow_image = pipe(image_path)  # applies mask on input and returns a pillow image
	pillow_image.save(output_path)
	print(f"Đã lưu ảnh desaturated tại: {output_path}")
	return output_path