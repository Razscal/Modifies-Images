import os
import uuid
from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from utils.image_process import main_process
import shutil
from fastapi.background import BackgroundTasks
import zipfile

router = APIRouter(
	prefix="/file",
	tags=["file"]
)

@router.post("/upload")
async def upload_file(background_task: BackgroundTasks, upload_file : UploadFile = File(...)):
	img_id = uuid.uuid4()
	step =0
	path = f"files/{img_id}_{step}.png"

	if not os.path.isdir("files"):
		os.mkdir("files")

	with open(path, "w+b") as buffer:
		shutil.copyfileobj(upload_file.file, buffer)
	print(f"Image {path} uploaded with ID {img_id}")

	background_task.add_task(main_process, img_id, path, step)

	return {
		"id" : str(img_id),
		"source" : "http://localhost:8000/files/",
		"status": "success",
		"message": "Image uploaded and is being processed"
	}


@router.get("/download")
async def download_file(id: str):
	directory = 'files'

	# List all files that start with 'id' in the 'files' directory
	files_to_append = [f for f in os.listdir(directory) if
	                   os.path.isfile(os.path.join(directory, f)) and f.startswith(id)]

	# If no files match the pattern, return a message
	if not files_to_append:
		return {
			"status": "failed",
			"message": "No files found to zip"
		}

	try:
		# Create or append to the zip file
		zip_filename = f'files/{id}_final.zip'
		mode = 'a' if os.path.exists(zip_filename) else 'w'

		with zipfile.ZipFile(zip_filename, mode) as zipf:
			for file in files_to_append:
				file_path = os.path.join(directory, file)  # Get the full file path
				zipf.write(file_path, arcname=file)  # Add file to the zip, store only the file name

	except Exception as e:
		print(e)
		return {
			"status": "failed",
			"message": "Failed to create zip file"
		}

	# Return the zip file for download
	return FileResponse(zip_filename)

@router.get("/download_step")
async def download_step(id,step):
	return FileResponse(f"files/{id}_{step}.png")