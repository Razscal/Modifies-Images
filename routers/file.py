import os
import uuid
from fastapi import APIRouter, FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import zipfile
from strategies import registry

router = APIRouter(
	prefix="/upload",
	tags=["upload"]
)

@router.post("/remove")
async def remove_background(upload_file: UploadFile = File(...)):
	return registry.get_registry("rmbg").action()

