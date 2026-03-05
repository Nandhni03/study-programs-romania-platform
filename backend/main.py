from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import json

# FastAPI app instance (required by uvicorn)
app = FastAPI(title="UVT Study Programs Map")

# Path helpers
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
DATA_FILE = BASE_DIR / "data/uvt_programs_raw.json"

# Serve frontend static files
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

# Route for root: serve index.html directly
@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")

# API endpoint: get all programs
@app.get("/programs")
def get_programs():
    if DATA_FILE.exists():
        with open(DATA_FILE, encoding="utf-8") as f:
            programs = json.load(f)
        return JSONResponse(content=programs)
    return JSONResponse(content=[], status_code=404)