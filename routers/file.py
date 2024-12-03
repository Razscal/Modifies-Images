import os
import uuid

from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from utils.image_process import main_process
import shutil
from fastapi.background import BackgroundTasks

router = APIRouter(
	prefix="/file",
	tags=["file"]
)

@router.post("/upload")
async def upload_file(background_task: BackgroundTasks, upload_file : UploadFile = File(...)):
	path = f"files/{uuid.uuid4()}_0.png"
	processed = f"processed_image/{uuid.uuid4()}_final.png"

	if not os.path.isdir("files"):
		os.mkdir("files")
	if not os.path.isdir("processed_image"):
		os.mkdir("processed_image")

	with open(path, "w+b") as buffer:
		shutil.copyfileobj(upload_file.file, buffer)

	background_task.add_task(main_process, path, processed)
	return {
		"status": "success",
		"message": "Image uploaded"
	}