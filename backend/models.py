from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any

class UserRegisterRequest(BaseModel):
    email: str
    full_name: str
    role: Optional[str] = "household"
    password: Optional[str] = "password123"
    phone: Optional[str] = ""
    address: Optional[str] = ""
    business_name: Optional[str] = ""
    categories: Optional[str] = ""

class UserLoginRequest(BaseModel):
    email: str
    password: Optional[str] = "password123"

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class HouseholdUpdateRequest(BaseModel):
    home_type: Optional[str] = None
    size_sqft: Optional[int] = None
    occupants: Optional[int] = None
    location: Optional[str] = None
    monthly_budget: Optional[float] = None
    solar_available: Optional[bool] = None

class HouseholdBillRequest(BaseModel):
    amount: Optional[float] = 0.0
    units: Optional[float] = 0.0
    billingPeriod: Optional[str] = None
    billing_period: Optional[str] = None
    tariffRate: Optional[float] = None
    tariff_rate: Optional[float] = None
    fixedCharges: Optional[float] = None
    fixed_charges: Optional[float] = None
    taxes: Optional[float] = 0.0
    otherCharges: Optional[float] = None
    other_charges: Optional[float] = None
    discom: Optional[str] = "Utility Provider"
    source: Optional[str] = "bill_analyzer"

class ApplianceCreateUpdateRequest(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = "Appliance"
    category: Optional[str] = "General"
    quantity: Optional[int] = 1
    power_rating_watts: Optional[float] = None
    power: Optional[float] = None
    usage_hours_per_day: Optional[float] = None
    hours: Optional[float] = None

class EnergyReadingRequest(BaseModel):
    household_id: Optional[int] = 1
    date: Optional[str] = None
    kwh: float
    source: Optional[str] = "Grid Meter"
    notes: Optional[str] = ""

class ConsumptionRequest(BaseModel):
    kwh: float
    date: Optional[str] = None

class ServiceRequestCreate(BaseModel):
    user_id: Optional[int] = 1
    provider_id: Optional[int] = 1
    service_type: Optional[str] = "Maintenance"
    description: Optional[str] = ""
    requested_date: Optional[str] = "2026-03-25"
    address: Optional[str] = "Mumbai"

class ServiceRequestStatusUpdate(BaseModel):
    status: str

class AIChatRequest(BaseModel):
    message: str
    user_id: Optional[int] = 1
    conversation_id: Optional[int] = None
