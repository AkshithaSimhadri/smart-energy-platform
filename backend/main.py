import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from backend.config import settings
from backend.routers import auth, users, appliances, energy, providers, ai

app = FastAPI(
    title="Smart Household Energy Management API",
    description="Python + FastAPI backend with MySQL, Mistral AI, and ML energy forecasting (Linear Regression, Random Forest, XGBoost)",
    version="2.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(appliances.router)
app.include_router(energy.router)
app.include_router(providers.router)
app.include_router(ai.router)

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "Smart Household Energy Management System",
        "backend": "Python + FastAPI",
        "database": "MySQL (smart_energy)",
        "ai_engine": "Mistral AI",
        "ml_forecasting_models": [
            "Linear Regression",
            "Random Forest",
            "XGBoost"
        ],
        "active_modules": [
            "1. Dashboard",
            "2. Electricity Bill Analyzer",
            "3. Energy Consumption & Forecasting",
            "4. Solar Potential / ROI",
            "5. Service Provider",
            "6. Before You Buy"
        ]
    }

# Serve React Vite Frontend (Static Assets & SPA Fallback)
DIST_DIR = Path(__file__).resolve().parent.parent / "dist"

if (DIST_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Do not intercept API requests
    if full_path.startswith("api/"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API endpoint not found")

    target_file = DIST_DIR / full_path
    if full_path and target_file.is_file():
        return FileResponse(str(target_file))

    index_html = DIST_DIR / "index.html"
    if index_html.is_file():
        return FileResponse(str(index_html))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Smart Household Energy FastAPI Backend is running.",
            "frontend_status": "Vite frontend building or dist/ not ready yet.",
            "api_health": "/api/health",
            "api_docs": "/docs",
        }
    )
