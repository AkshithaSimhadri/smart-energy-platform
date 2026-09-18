from fastapi import APIRouter, HTTPException, status
from backend.models import UserUpdateRequest, HouseholdUpdateRequest, HouseholdBillRequest
from backend.database import db

router = APIRouter(tags=["users_and_household"])

@router.get("/api/users/{user_id}")
def get_user(user_id: int):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {
        "id": user["id"],
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user["role"],
        "phone": user["phone"],
        "address": user["address"],
        "created_at": user["created_at"],
    }

@router.put("/api/users/{user_id}")
def update_user(user_id: int, req: UserUpdateRequest):
    updates = req.model_dump(exclude_unset=True)
    user = db.update_user(user_id, updates)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/api/household/{user_id}")
def get_household(user_id: int):
    return db.get_household_by_user_id(user_id)

@router.put("/api/household/{household_id}")
def update_household(household_id: int, req: HouseholdUpdateRequest):
    updates = req.model_dump(exclude_unset=True)
    return db.update_household(household_id, updates)

@router.get("/api/household/{household_id}/bill")
def get_household_bill(household_id: int):
    bill = db.get_household_bill(household_id)
    return bill or None

@router.post("/api/household/{household_id}/bill")
def save_household_bill(household_id: int, req: HouseholdBillRequest):
    data = req.model_dump(exclude_unset=True)
    bill = db.save_household_bill(household_id, data)
    return {
        "success": True,
        "bill": {
            "household_id": bill["household_id"],
            "amount": bill["amount"],
            "units": bill["units"],
            "billing_period": bill["billing_period"],
            "tariff_rate": bill["tariff_rate"],
            "fixed_charges": bill["fixed_charges"],
            "taxes": bill["taxes"],
            "other_charges": bill["other_charges"],
            "discom": bill["discom"],
            "source": bill["source"],
            "updated_at": bill["updated_at"],
        },
    }

@router.delete("/api/household/{household_id}/bill")
def delete_household_bill(household_id: int):
    db.delete_household_bill(household_id)
    return {"success": True}
