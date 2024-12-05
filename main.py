from fastapi import FastAPI, WebSocket
from routers import file
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(file.router)

origins = ["http://localhost:63343"]
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify your front-end domain)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.mount("/files", StaticFiles(directory="files"), name="files")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    img_id = None
    try:
        while True:
            data = await websocket.receive_text()
            if data:
                await websocket.send_text(f"WebSocket registered for image ID: {img_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")