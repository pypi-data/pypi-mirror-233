import os
import atexit
import tempfile
import subprocess
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from shutil import copytree, rmtree

def extract_static_files():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Register a cleanup function to remove the temp_dir on program exit
    atexit.register(rmtree, temp_dir)

    static_temp_dir = os.path.join(temp_dir, "aiconsole-static")
    
    # Directly specify the source directory
    source_dir = os.path.join(os.path.dirname(__file__), "web", "dist")
    copytree(source_dir, static_temp_dir)

    return static_temp_dir

# Build frontend
if os.path.exists(os.path.join("aiconsole", "web", "node_modules")):
    subprocess.run(["npm", "run", "build"], cwd=os.path.join("aiconsole", "web"))

static_dir = extract_static_files()

# Create FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

app.mount("/", StaticFiles(directory=static_dir))