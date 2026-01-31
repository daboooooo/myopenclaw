import sys
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Add the current directory to the path so we can import from api
sys.path.append(os.path.dirname(__file__))

from api.main import app as api_app
import uvicorn


# Create the main application
app = FastAPI(title="Modern Todo List Application", description="A beautiful and functional Todo List app")

# Mount the API routes under /api
app.mount("/api", api_app)

# Serve static files from the frontend directory
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    @app.get("/")
    def read_root():
        return {"message": "Modern Todo List API - Visit /api/docs for API documentation"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)