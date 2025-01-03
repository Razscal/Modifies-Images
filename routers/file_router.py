from fastapi import APIRouter, File, UploadFile
from strategies import registry

router = APIRouter(
	prefix="/upload",
	tags=["upload"]
)

@router.post("/remove")
async def remove_background(s3_url : str, bucket_name: str):
	return registry.get_strategy("rmbg").action(s3_url, bucket_name)

