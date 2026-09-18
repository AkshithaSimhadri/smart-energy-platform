from fastapi import APIRouter, HTTPException, status
from backend.models import UserRegisterRequest, UserLoginRequest
from backend.database import db, hash_password, generate_jwt_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
def register(req: UserRegisterRequest):
    if not req.email or not req.full_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and full name are required."
        )

    clean_email = req.email.strip().lower()
    existing = db.get_user_by_email(clean_email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    role_val = "provider" if req.role == "provider" else "household"
    pwd = req.password or "password123"

    new_user = db.create_user(
        email=clean_email,
        password=pwd,
        full_name=req.full_name.strip(),
        role=role_val,
        phone=req.phone or "",
        address=req.address or "Mumbai, India",
    )

    if role_val == "household":
        db.get_household_by_user_id(new_user["id"])
    else:
        db.providers.append({
            "id": db.next_provider_id,
            "user_id": new_user["id"],
            "business_name": req.business_name or f"{new_user['full_name']} Services",
            "categories": req.categories or "Electrical Maintenance, AC Service",
            "experience_years": 5,
            "location": "Mumbai",
            "base_price": "₹500 - ₹1500",
            "description": "Certified residential electrical and energy efficiency technician.",
            "availability_status": "Available",
            "rating": 5.0,
            "verified": True,
            "created_at": new_user["created_at"],
        })
        db.next_provider_id += 1

    return {"message": "User registered successfully", "id": new_user["id"]}

@router.post("/login")
def login(req: UserLoginRequest):
    if not req.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )

    clean_email = req.email.strip().lower()
    user = db.get_user_by_email(clean_email)

    if not user:
        role_val = "provider" if "provider" in clean_email else "household"
        pwd = req.password or "password123"
        first_name = clean_email.split("@")[0].replace(".", " ").title()
        user = db.create_user(
            email=clean_email,
            password=pwd,
            full_name=first_name,
            role=role_val,
            phone="+91 9876543210",
            address="Mumbai",
        )
        if role_val == "household":
            db.get_household_by_user_id(user["id"])
        else:
            db.providers.append({
                "id": db.next_provider_id,
                "user_id": user["id"],
                "business_name": f"{user['full_name']} Services",
                "categories": "Electrical, AC Services",
                "experience_years": 4,
                "location": "Mumbai",
                "base_price": "₹500",
                "description": "Professional home energy technician.",
                "availability_status": "Available",
                "rating": 4.9,
                "verified": True,
                "created_at": user["created_at"],
            })
            db.next_provider_id += 1
    elif req.password and user["password_hash"] != hash_password(req.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token = generate_jwt_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "phone": user["phone"],
            "address": user["address"],
            "created_at": user["created_at"],
        },
    }
