from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def use_cors(app: FastAPI):
	return app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],  # Allow all origins (or specify your front-end domain)
		allow_credentials=True,
		allow_methods=["*"],  # Allow all HTTP methods
		allow_headers=["*"],  # Allow all headers
	)
