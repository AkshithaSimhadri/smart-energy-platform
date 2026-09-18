import sys
import os
import subprocess
from pathlib import Path

root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

def ensure_dist_exists():
    dist_dir = root_dir / "dist"
    if not (dist_dir / "index.html").exists():
        print("[Build] Compiling React Vite frontend into dist/ ...")
        subprocess.run(["npx", "vite", "build"], check=True)

if __name__ == "__main__":
    ensure_dist_exists()
    import uvicorn
    from backend.main import app

    port = 3000
    print(f"[FastAPI] Starting Smart Household Energy backend on 0.0.0.0:{port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

