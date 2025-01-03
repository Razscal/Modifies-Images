from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

def use_static(app: FastAPI):
	app.mount("/static", StaticFiles(directory="static"), name="static")