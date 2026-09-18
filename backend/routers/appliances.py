from fastapi import APIRouter, HTTPException, status
from typing import List
from backend.models import ApplianceCreateUpdateRequest
from backend.database import db

router = APIRouter(tags=["appliances"])

@router.get("/api/household/{household_id}/appliances")
def get_appliances(household_id: int):
    return db.get_appliances(household_id)

@router.post("/api/household/{household_id}/appliances")
def add_appliance(household_id: int, req: ApplianceCreateUpdateRequest):
    data = req.model_dump(exclude_unset=True)
    return db.add_or_update_appliance(household_id, data)

@router.put("/api/household/{household_id}/appliances/{app_id}")
def update_appliance(household_id: int, app_id: int, req: ApplianceCreateUpdateRequest):
    data = req.model_dump(exclude_unset=True)
    updated = db.update_appliance(app_id, data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appliance not found")
    return updated

@router.delete("/api/household/{household_id}/appliances/{app_id}")
def delete_household_appliance(household_id: int, app_id: int):
    db.delete_appliance(app_id)
    return {"success": True, "id": app_id}

@router.delete("/api/appliances/{app_id}")
def delete_appliance(app_id: int):
    db.delete_appliance(app_id)
    return {"success": True, "id": app_id}
