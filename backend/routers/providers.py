from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional, List
from backend.models import ServiceRequestCreate, ServiceRequestStatusUpdate
from backend.database import db

router = APIRouter(tags=["providers_and_services"])

@router.get("/api/providers")
def list_providers(
    category: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    return db.get_providers(category=category, location=location, search=search)

@router.get("/api/providers/{user_id}")
def get_provider(user_id: int):
    p = db.get_provider_by_user_id(user_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    return p

@router.put("/api/providers/{provider_id}")
def update_provider(provider_id: int, updates: dict):
    p = db.update_provider(provider_id, updates)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found")
    return p

@router.post("/api/service-requests")
def create_service_request(req: ServiceRequestCreate):
    return db.create_service_request(
        user_id=req.user_id or 1,
        provider_id=req.provider_id or 1,
        service_type=req.service_type or "Maintenance",
        description=req.description or "",
        requested_date=req.requested_date or "2026-03-25",
        address=req.address or "Mumbai",
    )

@router.get("/api/service-requests/user/{user_id}")
def get_user_service_requests(user_id: int):
    return db.get_service_requests_by_user(user_id)

@router.get("/api/service-requests/provider/{provider_id}")
def get_provider_service_requests(provider_id: int):
    return db.get_service_requests_by_provider(provider_id)

@router.put("/api/service-requests/{request_id}/status")
def update_status_put(request_id: int, body: ServiceRequestStatusUpdate):
    updated = db.update_service_request_status(request_id, body.status)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return updated

@router.patch("/api/service-requests/{request_id}/status")
def update_status_patch(request_id: int, body: ServiceRequestStatusUpdate):
    updated = db.update_service_request_status(request_id, body.status)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return updated
