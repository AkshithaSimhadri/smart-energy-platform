from fastapi import APIRouter, HTTPException, status, UploadFile, File, Response, Query
from typing import Optional
from datetime import datetime
from backend.models import EnergyReadingRequest, ConsumptionRequest
from backend.database import db
from backend.ml_forecasting import (
    generate_forecast_ml,
    build_monthly_energy_summary,
    generate_formatted_csv
)

router = APIRouter(prefix="/api/energy", tags=["energy"])

def _get_readings_internal(household_id: int):
    return db.get_readings(household_id)

@router.get("/readings")
def get_readings_default():
    return _get_readings_internal(1)

@router.get("/readings/{household_id}")
def get_readings(household_id: int):
    return _get_readings_internal(household_id)

def _add_reading_internal(household_id: int, req: EnergyReadingRequest):
    if req.kwh < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consumption (kWh) must be a non-negative number."
        )
    date_str = req.date or datetime.now().strftime("%Y-%m-%d")
    source = req.source or "Grid Meter"
    notes = req.notes or ""
    return db.add_reading(household_id, date_str, req.kwh, source, notes)

@router.post("/readings")
def add_reading_default(req: EnergyReadingRequest):
    hh_id = req.household_id or 1
    return _add_reading_internal(hh_id, req)

@router.post("/readings/{household_id}")
def add_reading(household_id: int, req: EnergyReadingRequest):
    return _add_reading_internal(household_id, req)

@router.delete("/readings/{reading_id}")
def delete_reading(reading_id: int):
    deleted = db.delete_reading(reading_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found")
    return {"message": "Reading deleted successfully", "id": reading_id}

@router.post("/consumption/{household_id}")
def add_consumption(household_id: int, req: ConsumptionRequest):
    if req.kwh < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consumption cannot be negative."
        )
    date_str = req.date or datetime.now().strftime("%Y-%m-%d")
    reading = db.add_reading(household_id, date_str, req.kwh, "Grid Meter", "")
    return {
        "message": "Consumption added",
        "id": reading["id"],
        "reading": {
            "id": reading["id"],
            "household_id": reading["household_id"],
            "date": reading["date"],
            "kwh": reading["kwh"],
            "source": reading["source"],
        },
    }

def _generate_forecast_internal(household_id: int):
    readings = db.get_readings(household_id)
    data_points = [{"date_str": r["date"], "kwh": r["kwh"]} for r in readings]
    return generate_forecast_ml(data_points, days=30)

@router.get("/forecast")
def get_forecast_default():
    return _generate_forecast_internal(1)

@router.get("/forecast/{household_id}")
def get_forecast(household_id: int):
    return _generate_forecast_internal(household_id)

@router.post("/forecast")
def post_forecast_default():
    return _generate_forecast_internal(1)

@router.post("/forecast/{household_id}")
def post_forecast(household_id: int):
    return _generate_forecast_internal(household_id)

@router.post("/forecast/upload")
async def upload_forecast_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please upload a CSV file."
        )

    content_bytes = await file.read()
    content = content_bytes.decode("utf-8", errors="ignore")
    raw_lines = [line.strip() for line in content.splitlines() if line.strip()]

    if len(raw_lines) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded CSV contains no records."
        )

    header = [col.strip().lower().replace('"', '').replace("'", "") for col in raw_lines[0].split(",")]

    date_col = 0
    for idx, col in enumerate(header):
        if col in ["timestamp", "date", "datetime", "time"]:
            date_col = idx
            break

    kwh_col = len(header) - 1
    for idx, col in enumerate(header):
        if col in ["kwh", "consumption", "units", "energy", "predicted_kwh"]:
            kwh_col = idx
            break

    data_points = []
    for line in raw_lines[1:]:
        parts = [p.strip().replace('"', '').replace("'", "") for p in line.split(",")]
        if len(parts) > max(date_col, kwh_col):
            try:
                val = float(parts[kwh_col])
                if val >= 0:
                    data_points.append({"date_str": parts[date_col], "kwh": val})
            except ValueError:
                continue

    if len(data_points) < 15:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded CSV must contain at least 15 records of historical energy data."
        )

    # Train and evaluate Linear Regression, Random Forest, and XGBoost on user dataset
    result = generate_forecast_ml(data_points, days=30)
    result["data_source"] = "user_dataset"
    result["uploaded_file"] = file.filename
    result["uploaded_records"] = len(data_points)
    return result

def _get_monthly_summary_internal(household_id: int, tariff_rate: float, include_forecast: bool):
    return build_monthly_energy_summary(household_id, db, tariff_rate=tariff_rate, include_forecast=include_forecast)

@router.get("/monthly-summary")
def get_monthly_summary_default(
    tariff_rate: float = Query(7.5),
    include_forecast: bool = Query(True)
):
    return _get_monthly_summary_internal(1, tariff_rate, include_forecast)

@router.get("/monthly-summary/{household_id}")
def get_monthly_summary(
    household_id: int,
    tariff_rate: float = Query(7.5),
    include_forecast: bool = Query(True)
):
    return _get_monthly_summary_internal(household_id, tariff_rate, include_forecast)

def _download_csv_internal(household_id: int, tariff_rate: float, include_forecast: bool):
    summary_data = build_monthly_energy_summary(household_id, db, tariff_rate=tariff_rate, include_forecast=include_forecast)
    csv_text = generate_formatted_csv(summary_data)
    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"monthly_energy_consumption_summary_household_{household_id}_{today_str}.csv"

    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache",
        }
    )

@router.get("/monthly-summary/csv")
def download_monthly_summary_csv_default(
    tariff_rate: float = Query(7.5),
    include_forecast: bool = Query(True)
):
    return _download_csv_internal(1, tariff_rate, include_forecast)

@router.get("/monthly-summary/csv/{household_id}")
def download_monthly_summary_csv(
    household_id: int,
    tariff_rate: float = Query(7.5),
    include_forecast: bool = Query(True)
):
    return _download_csv_internal(household_id, tariff_rate, include_forecast)

@router.get("/download-csv")
def download_csv_default(
    tariff_rate: float = Query(7.5),
    include_forecast: bool = Query(True)
):
    return _download_csv_internal(1, tariff_rate, include_forecast)

@router.get("/download-csv/{household_id}")
def download_csv(
    household_id: int,
    tariff_rate: float = Query(7.5),
    include_forecast: bool = Query(True)
):
    return _download_csv_internal(household_id, tariff_rate, include_forecast)
