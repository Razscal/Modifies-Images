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
async def download_file(id):
	return FileResponse(f"files/{id}_final.png")

@router.get("/download_step")
async def download_step(id,step):
	return FileResponse(f"files/{id}_{step}.png")