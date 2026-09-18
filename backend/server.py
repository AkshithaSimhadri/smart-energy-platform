import os
import sys
from pathlib import Path

# Add current working directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import uvicorn
from backend.main import app

if __name__ == "__main__":
    # Always bind strictly to port 3000 on 0.0.0.0
    port = 3000
    print(f"[FastAPI] Starting Smart Household Energy backend on 0.0.0.0:{port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
