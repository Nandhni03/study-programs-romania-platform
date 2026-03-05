from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import json

app = FastAPI(title="UVT Study Programs Map")

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "uvt_programs_raw.json"

# Mount static folders
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")
app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")

@app.get("/")
def root():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return JSONResponse({"error": "index.html not found"}, status_code=404)

@app.get("/programs")
def get_programs():
    if DATA_FILE.exists():
        with open(DATA_FILE, encoding="utf-8") as f:
            programs = json.load(f)
        return JSONResponse(content=programs)
    return JSONResponse(content=[], status_code=404)