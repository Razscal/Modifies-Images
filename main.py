import uvicorn
from fastapi import FastAPI
from routers import file_router
from middleware.use_cors import use_cors
from middleware.use_static import use_static

app = FastAPI()
app.include_router(file_router.router)

# Configure CORS
use_static(app)
use_cors(app)

@app.get("/")
async def root():
	return {"message": "Hello, World!"}


if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)
