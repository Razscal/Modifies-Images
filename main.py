from fastapi import FastAPI
from routers import file
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(file.router)

origins = ["https://localhost:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])

