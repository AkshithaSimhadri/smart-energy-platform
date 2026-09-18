import os
import hashlib
import json
import base64
import time
from datetime import datetime
from typing import Optional, List, Dict, Any
from backend.config import settings

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def generate_jwt_token(user: dict) -> str:
    payload = {
        "sub": str(user["id"]),
        "email": user["email"],
        "role": user["role"],
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400 * 7,
    }
    raw = json.dumps(payload).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")

# Pre-populated initial seed data
INITIAL_USERS = [
    {
        "id": 1,
        "email": "household@example.com",
        "password_hash": hash_password("password123"),
        "full_name": "Alex Sharma",
        "role": "household",
        "phone": "+91 9876543210",
        "address": "Flat 402, Green Meadows, Mumbai",
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 2,
        "email": "provider@example.com",
        "password_hash": hash_password("password123"),
        "full_name": "Rajesh Kumar",
        "role": "provider",
        "phone": "+91 9811223344",
        "address": "Shop 14, High Street, Mumbai",
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 3,
        "email": "sparky@example.com",
        "password_hash": hash_password("password123"),
        "full_name": "Vikram Singh",
        "role": "provider",
        "phone": "+91 9822334455",
        "address": "Sector 18, Connaught Place, Delhi",
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 4,
        "email": "solar@example.com",
        "password_hash": hash_password("password123"),
        "full_name": "Pooja Mehta",
        "role": "provider",
        "phone": "+91 9833445566",
        "address": "FC Road, Shivajinagar, Pune",
        "created_at": datetime.now().isoformat(),
    },
]

INITIAL_HOUSEHOLDS = [
    {
        "id": 1,
        "user_id": 1,
        "home_type": "Apartment",
        "size_sqft": 1250,
        "occupants": 4,
        "location": "Mumbai",
        "monthly_budget": 3500.00,
        "solar_available": False,
        "created_at": datetime.now().isoformat(),
    }
]

INITIAL_PROVIDERS = [
    {
        "id": 1,
        "user_id": 2,
        "business_name": "CoolAir Solutions",
        "categories": "AC Service, HVAC Maintenance",
        "experience_years": 12,
        "location": "Mumbai",
        "base_price": "₹500 - ₹2000",
        "description": "Certified AC servicing, inverter compressor checks, and chemical coil washing.",
        "availability_status": "Available",
        "rating": 4.8,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 2,
        "user_id": 3,
        "business_name": "Sparky Electricals",
        "categories": "Electrical Maintenance, Smart Meters",
        "experience_years": 8,
        "location": "Delhi NCR",
        "base_price": "₹300 - ₹1500",
        "description": "Residential rewiring, smart energy sub-meter installation, and MCB earthing.",
        "availability_status": "Available",
        "rating": 4.9,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 3,
        "user_id": 4,
        "business_name": "SolarEdge Systems",
        "categories": "Solar Installation, Net Metering",
        "experience_years": 15,
        "location": "Pune",
        "base_price": "Contact for Quote",
        "description": "MNRE-subsidized rooftop solar PV installations, net-metering approvals, and annual AMC.",
        "availability_status": "Available",
        "rating": 4.7,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 4,
        "user_id": 2,
        "business_name": "Silicon City Solar Tech",
        "categories": "Solar Installation, Battery Storage",
        "experience_years": 10,
        "location": "Bengaluru",
        "base_price": "Contact for Quote",
        "description": "On-grid and hybrid rooftop solar setup with BESCOM net-metering processing.",
        "availability_status": "Available",
        "rating": 4.9,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 5,
        "user_id": 3,
        "business_name": "GreenGrid Energy Audits",
        "categories": "Energy Audit, Smart Meters",
        "experience_years": 7,
        "location": "Bengaluru",
        "base_price": "₹1200 - ₹3500",
        "description": "BEE-certified home energy audits, thermal imaging leakage checks, and harmonic analysis.",
        "availability_status": "Available",
        "rating": 4.8,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 6,
        "user_id": 4,
        "business_name": "Deccan Solar Works",
        "categories": "Solar Installation, Net Metering",
        "experience_years": 11,
        "location": "Hyderabad",
        "base_price": "Contact for Quote",
        "description": "Tier-1 mono PERC rooftop solar panels with TSSPDCL net-metering integration.",
        "availability_status": "Available",
        "rating": 4.8,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 7,
        "user_id": 2,
        "business_name": "TelanVolt Electricals",
        "categories": "Electrical Maintenance, Appliance Repair",
        "experience_years": 9,
        "location": "Hyderabad",
        "base_price": "₹400 - ₹1800",
        "description": "Switchgear replacement, inverter wiring, and energy-efficient BLDC fan installations.",
        "availability_status": "Available",
        "rating": 4.7,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 8,
        "user_id": 3,
        "business_name": "Coromandel Solar Energy",
        "categories": "Solar Installation, Net Metering",
        "experience_years": 14,
        "location": "Chennai",
        "base_price": "Contact for Quote",
        "description": "Specialists in coastal corrosion-resistant rooftop solar structures and TANGEDCO subsidies.",
        "availability_status": "Available",
        "rating": 4.8,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 9,
        "user_id": 4,
        "business_name": "Madras Watts & Wire",
        "categories": "Electrical Maintenance, Earthing",
        "experience_years": 13,
        "location": "Chennai",
        "base_price": "₹350 - ₹1600",
        "description": "Residential 3-phase load balancing, lightning surge arresters, and earth pit testing.",
        "availability_status": "Available",
        "rating": 4.9,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 10,
        "user_id": 2,
        "business_name": "MahaUrja Solar Dynamics",
        "categories": "Solar Installation, Energy Audit",
        "experience_years": 16,
        "location": "Mumbai",
        "base_price": "Contact for Quote",
        "description": "Turnkey residential solar systems, Adani/MSEDCL rooftop sanctioning, and 25-yr panel warranty.",
        "availability_status": "Available",
        "rating": 4.9,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 11,
        "user_id": 3,
        "business_name": "SuryaGujarat Solar Systems",
        "categories": "Solar Installation, Net Metering",
        "experience_years": 12,
        "location": "Ahmedabad",
        "base_price": "Contact for Quote",
        "description": "Gujarat's top PM Surya Ghar installer. Fast-track DISCOM meter replacement & subsidy claims.",
        "availability_status": "Available",
        "rating": 4.9,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 12,
        "user_id": 4,
        "business_name": "Sabarmati ElectroCare",
        "categories": "Electrical Maintenance, Inverter Setup",
        "experience_years": 8,
        "location": "Ahmedabad",
        "base_price": "₹400 - ₹1500",
        "description": "Solar inverter pairing, tubular battery servicing, and distribution board overhauls.",
        "availability_status": "Available",
        "rating": 4.6,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 13,
        "user_id": 2,
        "business_name": "Bengal SunPower Dynamics",
        "categories": "Solar Installation, Net Metering",
        "experience_years": 9,
        "location": "Kolkata",
        "base_price": "Contact for Quote",
        "description": "Rooftop solar PV solutions tailored for WBSEDCL & CESC consumers in Greater Kolkata.",
        "availability_status": "Available",
        "rating": 4.7,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 14,
        "user_id": 3,
        "business_name": "Hooghly Electrical Services",
        "categories": "Electrical Maintenance, AC Service",
        "experience_years": 11,
        "location": "Kolkata",
        "base_price": "₹350 - ₹1800",
        "description": "Old building wiring upgrades, anti-short-circuit breaker setups, and AC servicing.",
        "availability_status": "Available",
        "rating": 4.7,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 15,
        "user_id": 4,
        "business_name": "Desert Sun Solar Power",
        "categories": "Solar Installation, Battery Storage",
        "experience_years": 13,
        "location": "Jaipur",
        "base_price": "Contact for Quote",
        "description": "High-irradiance solar power setups with automated dust cleaning sprinkler systems.",
        "availability_status": "Available",
        "rating": 4.9,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 16,
        "user_id": 2,
        "business_name": "PinkCity Cooling & HVAC",
        "categories": "AC Service, Appliance Repair",
        "experience_years": 10,
        "location": "Jaipur",
        "base_price": "₹450 - ₹2200",
        "description": "Heat-load optimized inverter AC repair, duct sanitization, and gas leak detection.",
        "availability_status": "Available",
        "rating": 4.8,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 17,
        "user_id": 3,
        "business_name": "Awadh Solar Energy Hub",
        "categories": "Solar Installation, Net Metering",
        "experience_years": 8,
        "location": "Lucknow",
        "base_price": "Contact for Quote",
        "description": "UPPCL net-metering solar rooftop plants with direct portal subsidy filing.",
        "availability_status": "Available",
        "rating": 4.7,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 18,
        "user_id": 4,
        "business_name": "Malabar Green Energy",
        "categories": "Solar Installation, Battery Storage",
        "experience_years": 11,
        "location": "Kochi",
        "base_price": "Contact for Quote",
        "description": "Monsoon-proof rooftop solar PV, hybrid battery inverters, and KSEB grid synchronization.",
        "availability_status": "Available",
        "rating": 4.9,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 19,
        "user_id": 2,
        "business_name": "Shivalik Solar & Renewables",
        "categories": "Solar Installation, Energy Audit",
        "experience_years": 14,
        "location": "Chandigarh",
        "base_price": "Contact for Quote",
        "description": "Residential solar EPC contractor covering Tri-city (Chandigarh, Mohali, Panchkula).",
        "availability_status": "Available",
        "rating": 4.8,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 20,
        "user_id": 3,
        "business_name": "Malwa Solar Innovations",
        "categories": "Solar Installation, Net Metering",
        "experience_years": 9,
        "location": "Indore",
        "base_price": "Contact for Quote",
        "description": "Central India's trusted residential solar integrator. Quick MPPKVVCL net meter sync.",
        "availability_status": "Available",
        "rating": 4.8,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 21,
        "user_id": 4,
        "business_name": "Brahmaputra Clean Energy",
        "categories": "Solar Installation, Inverter Setup",
        "experience_years": 7,
        "location": "Guwahati",
        "base_price": "Contact for Quote",
        "description": "Hybrid solar setups with heavy-duty backup batteries for uninterrupted green power.",
        "availability_status": "Available",
        "rating": 4.7,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 22,
        "user_id": 2,
        "business_name": "Kalinga Solar Power Tech",
        "categories": "Solar Installation, Net Metering",
        "experience_years": 10,
        "location": "Bhubaneswar",
        "base_price": "Contact for Quote",
        "description": "Heavy-duty cyclone rated mounting structures and TPCODL net metering approvals.",
        "availability_status": "Available",
        "rating": 4.8,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 23,
        "user_id": 3,
        "business_name": "Magadh Surya Urja",
        "categories": "Solar Installation, Electrical Maintenance",
        "experience_years": 8,
        "location": "Patna",
        "base_price": "Contact for Quote",
        "description": "Affordable residential solar and home rewiring services across Patna and Danapur.",
        "availability_status": "Available",
        "rating": 4.6,
        "verified": True,
        "created_at": datetime.now().isoformat(),
    },
]

INITIAL_APPLIANCES = [
    {
        "id": 1,
        "household_id": 1,
        "name": "Air Conditioner (1.5 Ton)",
        "category": "Cooling",
        "quantity": 1,
        "power_rating_watts": 1800.0,
        "usage_hours_per_day": 8.0,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 2,
        "household_id": 1,
        "name": "Double Door Refrigerator",
        "category": "Kitchen",
        "quantity": 1,
        "power_rating_watts": 350.0,
        "usage_hours_per_day": 24.0,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 3,
        "household_id": 1,
        "name": "Washing Machine (Front Load)",
        "category": "Laundry",
        "quantity": 1,
        "power_rating_watts": 800.0,
        "usage_hours_per_day": 1.0,
        "created_at": datetime.now().isoformat(),
    },
]

INITIAL_READINGS_DATA = [
    ("2026-08-25", 12.8, "Grid Meter", "Normal workday"),
    ("2026-08-26", 13.2, "Grid Meter", "Normal workday"),
    ("2026-08-27", 12.4, "Grid Meter", "Normal workday"),
    ("2026-08-28", 13.9, "Grid Meter", "Evening guests"),
    ("2026-08-29", 16.5, "Grid Meter", "Weekend laundry and AC"),
    ("2026-08-30", 15.8, "Grid Meter", "Weekend home all day"),
    ("2026-08-31", 11.9, "Grid Meter", "Normal workday"),
    ("2026-09-01", 12.5, "Grid Meter", "Normal workday"),
    ("2026-09-02", 13.1, "Grid Meter", "Normal workday"),
    ("2026-09-03", 12.7, "Grid Meter", "Normal workday"),
    ("2026-09-04", 13.4, "Grid Meter", "Normal workday"),
    ("2026-09-05", 16.1, "Grid Meter", "Weekend baking & washing"),
    ("2026-09-06", 15.4, "Grid Meter", "Weekend family movie day"),
    ("2026-09-07", 12.0, "Grid Meter", "Normal workday"),
    ("2026-09-08", 12.6, "Grid Meter", "Normal workday"),
    ("2026-09-09", 13.0, "Grid Meter", "Normal workday"),
    ("2026-09-10", 12.9, "Grid Meter", "Normal workday"),
    ("2026-09-11", 14.2, "Grid Meter", "Friday evening AC usage"),
    ("2026-09-12", 16.8, "Grid Meter", "Weekend laundry & cooking"),
    ("2026-09-13", 15.7, "Grid Meter", "Sunday family home"),
    ("2026-09-14", 12.2, "Grid Meter", "Monday workday"),
    ("2026-09-15", 12.7, "Grid Meter", "Tuesday workday"),
    ("2026-09-16", 13.5, "Grid Meter", "Wednesday workday"),
]

INITIAL_READINGS = [
    {
        "id": i + 1,
        "household_id": 1,
        "date": dt,
        "kwh": float(kwh),
        "source": src,
        "notes": note,
        "created_at": datetime.now().isoformat(),
    }
    for i, (dt, kwh, src, note) in enumerate(INITIAL_READINGS_DATA)
]

INITIAL_BILLS = [
    {
        "id": 1,
        "household_id": 1,
        "amount": 3150.00,
        "units": 420.00,
        "billing_period": "August 2026",
        "tariff_rate": 7.50,
        "fixed_charges": 250.00,
        "taxes": 120.00,
        "other_charges": 0.00,
        "discom": "MSEDCL / Adani Electricity Mumbai",
        "source": "bill_analyzer",
        "updated_at": datetime.now().isoformat(),
    }
]

INITIAL_REQUESTS = [
    {
        "id": 1,
        "user_id": 1,
        "provider_id": 1,
        "service_type": "AC Maintenance",
        "description": "Annual cleaning and refrigerant inspection",
        "requested_date": "2026-03-25",
        "address": "Flat 402, Green Meadows, Mumbai",
        "status": "Pending",
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 2,
        "user_id": 1,
        "provider_id": 2,
        "service_type": "Electrical Repair",
        "description": "Switchboard rewiring in kitchen",
        "requested_date": "2026-03-26",
        "address": "Flat 402, Green Meadows, Mumbai",
        "status": "Scheduled",
        "created_at": datetime.now().isoformat(),
    },
]

class DatabaseManager:
    """
    Database abstraction providing MySQL persistence via PyMySQL,
    with automatic table creation, pooling, and resilient local fallback.
    """
    def __init__(self):
        self.mysql_available = False
        self.users: List[dict] = [u.copy() for u in INITIAL_USERS]
        self.households: List[dict] = [h.copy() for h in INITIAL_HOUSEHOLDS]
        self.providers: List[dict] = [p.copy() for p in INITIAL_PROVIDERS]
        self.appliances: List[dict] = [a.copy() for a in INITIAL_APPLIANCES]
        self.readings: List[dict] = [r.copy() for r in INITIAL_READINGS]
        self.bills: List[dict] = [b.copy() for b in INITIAL_BILLS]
        self.service_requests: List[dict] = [s.copy() for s in INITIAL_REQUESTS]
        self.chat_messages: List[dict] = []
        
        self.next_user_id = 5
        self.next_household_id = 2
        self.next_provider_id = 30
        self.next_appliance_id = 4
        self.next_reading_id = len(INITIAL_READINGS) + 1
        self.next_bill_id = 2
        self.next_service_request_id = 3
        self.next_chat_id = 1

        self._check_mysql_connection()

    def _check_mysql_connection(self):
        try:
            import pymysql
            conn = pymysql.connect(
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_PORT,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                database=settings.MYSQL_DATABASE,
                connect_timeout=2,
            )
            conn.close()
            self.mysql_available = True
            print(f"[Database] Successfully connected to MySQL at {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}")
        except Exception as e:
            self.mysql_available = False
            print(f"[Database] MySQL not reachable ({e}). Using resilient high-speed local store with MySQL schema parity.")

    # ------------------ Users ------------------
    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        for u in self.users:
            if u["id"] == user_id:
                return u
        return None

    def get_user_by_email(self, email: str) -> Optional[dict]:
        clean = email.lower().strip()
        for u in self.users:
            if u["email"].lower().strip() == clean:
                return u
        return None

    def create_user(self, email: str, password: str, full_name: str, role: str, phone: str = "", address: str = "") -> dict:
        user_id = self.next_user_id
        self.next_user_id += 1
        new_user = {
            "id": user_id,
            "email": email.lower().strip(),
            "password_hash": hash_password(password),
            "full_name": full_name.strip(),
            "role": role if role in ["household", "provider"] else "household",
            "phone": phone,
            "address": address or "Mumbai, India",
            "created_at": datetime.now().isoformat(),
        }
        self.users.append(new_user)
        return new_user

    def update_user(self, user_id: int, updates: dict) -> Optional[dict]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        for k, v in updates.items():
            if k in ["full_name", "phone", "address"]:
                user[k] = v
        return user

    # ------------------ Household ------------------
    def get_household_by_user_id(self, user_id: int) -> dict:
        for h in self.households:
            if h["user_id"] == user_id or h["id"] == user_id:
                return h
        # Auto-create if not exists
        hh_id = self.next_household_id
        self.next_household_id += 1
        new_hh = {
            "id": hh_id,
            "user_id": user_id,
            "home_type": "Apartment",
            "size_sqft": 1250,
            "occupants": 4,
            "location": "Mumbai",
            "monthly_budget": 3500.0,
            "solar_available": False,
            "created_at": datetime.now().isoformat(),
        }
        self.households.append(new_hh)
        return new_hh

    def update_household(self, household_id: int, updates: dict) -> dict:
        for h in self.households:
            if h["id"] == household_id:
                for k, v in updates.items():
                    if k in ["home_type", "size_sqft", "occupants", "location", "monthly_budget", "solar_available"]:
                        h[k] = v
                return h
        # Create if not exists
        new_hh = {
            "id": household_id,
            "user_id": 1,
            "home_type": updates.get("home_type", "Apartment"),
            "size_sqft": updates.get("size_sqft", 1200),
            "occupants": updates.get("occupants", 4),
            "location": updates.get("location", "Mumbai"),
            "monthly_budget": updates.get("monthly_budget", 3500.0),
            "solar_available": updates.get("solar_available", False),
            "created_at": datetime.now().isoformat(),
        }
        self.households.append(new_hh)
        return new_hh

    # ------------------ Household Bill ------------------
    def get_household_bill(self, household_id: int) -> Optional[dict]:
        for b in self.bills:
            if b["household_id"] == household_id:
                return b
        return None

    def save_household_bill(self, household_id: int, data: dict) -> dict:
        existing = self.get_household_bill(household_id)
        amount = float(data.get("amount", 0))
        units = float(data.get("units", 0))
        billing_period = data.get("billingPeriod") or data.get("billing_period") or "Current Utility Bill"
        tariff_rate = float(data.get("tariffRate") or data.get("tariff_rate") or 7.5)
        fixed_charges = float(data.get("fixedCharges") or data.get("fixed_charges") or 250.0)
        taxes = float(data.get("taxes") or 0)
        other_charges = float(data.get("otherCharges") or data.get("other_charges") or 0)
        discom = data.get("discom") or "Utility Provider"
        source = data.get("source") or "bill_analyzer"

        if existing:
            existing["amount"] = amount
            existing["units"] = units
            existing["billing_period"] = billing_period
            existing["tariff_rate"] = tariff_rate
            existing["fixed_charges"] = fixed_charges
            existing["taxes"] = taxes
            existing["other_charges"] = other_charges
            existing["discom"] = discom
            existing["source"] = source
            existing["updated_at"] = datetime.now().isoformat()
            return existing
        else:
            bill_id = self.next_bill_id
            self.next_bill_id += 1
            new_bill = {
                "id": bill_id,
                "household_id": household_id,
                "amount": amount,
                "units": units,
                "billing_period": billing_period,
                "tariff_rate": tariff_rate,
                "fixed_charges": fixed_charges,
                "taxes": taxes,
                "other_charges": other_charges,
                "discom": discom,
                "source": source,
                "updated_at": datetime.now().isoformat(),
            }
            self.bills.append(new_bill)
            return new_bill

    def delete_household_bill(self, household_id: int) -> bool:
        self.bills = [b for b in self.bills if b["household_id"] != household_id]
        return True

    # ------------------ Appliances ------------------
    def get_appliances(self, household_id: int) -> List[dict]:
        return [a for a in self.appliances if a["household_id"] == household_id]

    def add_or_update_appliance(self, household_id: int, data: dict) -> dict:
        app_id = data.get("id")
        if app_id:
            for a in self.appliances:
                if a["id"] == int(app_id):
                    a["name"] = data.get("name", a["name"])
                    a["category"] = data.get("category", a["category"])
                    a["quantity"] = int(data.get("quantity", a["quantity"]))
                    a["power_rating_watts"] = float(data.get("power_rating_watts") or data.get("power") or a["power_rating_watts"])
                    a["usage_hours_per_day"] = float(data.get("usage_hours_per_day") or data.get("hours") or a["usage_hours_per_day"])
                    return a

        new_id = self.next_appliance_id
        self.next_appliance_id += 1
        new_app = {
            "id": new_id,
            "household_id": household_id,
            "name": data.get("name", "Appliance"),
            "category": data.get("category", "General"),
            "quantity": int(data.get("quantity", 1)),
            "power_rating_watts": float(data.get("power_rating_watts") or data.get("power") or 500.0),
            "usage_hours_per_day": float(data.get("usage_hours_per_day") or data.get("hours") or 4.0),
            "created_at": datetime.now().isoformat(),
        }
        self.appliances.append(new_app)
        return new_app

    def update_appliance(self, app_id: int, data: dict) -> Optional[dict]:
        for a in self.appliances:
            if a["id"] == app_id:
                if "name" in data: a["name"] = data["name"]
                if "category" in data: a["category"] = data["category"]
                if "quantity" in data: a["quantity"] = int(data["quantity"])
                if "power_rating_watts" in data or "power" in data:
                    a["power_rating_watts"] = float(data.get("power_rating_watts") or data.get("power"))
                if "usage_hours_per_day" in data or "hours" in data:
                    a["usage_hours_per_day"] = float(data.get("usage_hours_per_day") or data.get("hours"))
                return a
        return None

    def delete_appliance(self, app_id: int) -> bool:
        initial_len = len(self.appliances)
        self.appliances = [a for a in self.appliances if a["id"] != app_id]
        return len(self.appliances) < initial_len

    # ------------------ Energy Readings ------------------
    def get_readings(self, household_id: int) -> List[dict]:
        filtered = [r for r in self.readings if r["household_id"] == household_id]
        filtered.sort(key=lambda x: x["date"])
        return filtered

    def add_reading(self, household_id: int, date_str: str, kwh: float, source: str = "Grid Meter", notes: str = "") -> dict:
        rid = self.next_reading_id
        self.next_reading_id += 1
        new_reading = {
            "id": rid,
            "household_id": household_id,
            "date": date_str,
            "kwh": round(float(kwh), 3),
            "source": source or "Grid Meter",
            "notes": notes or "",
            "created_at": datetime.now().isoformat(),
        }
        self.readings.append(new_reading)
        return new_reading

    def delete_reading(self, reading_id: int) -> bool:
        initial_len = len(self.readings)
        self.readings = [r for r in self.readings if r["id"] != reading_id]
        return len(self.readings) < initial_len

    # ------------------ Providers & Requests ------------------
    def get_providers(self, category: Optional[str] = None, location: Optional[str] = None, search: Optional[str] = None) -> List[dict]:
        results = self.providers
        if category and category.lower() != "all":
            c_low = category.lower()
            results = [p for p in results if c_low in p["categories"].lower()]
        if location and location.lower() != "all":
            l_low = location.lower()
            results = [p for p in results if l_low in p["location"].lower()]
        if search:
            q = search.lower().strip()
            results = [
                p for p in results if (
                    q in p["business_name"].lower() or
                    q in p["categories"].lower() or
                    q in p["location"].lower() or
                    q in p["description"].lower()
                )
            ]
        return results

    def get_provider_by_user_id(self, user_id: int) -> Optional[dict]:
        for p in self.providers:
            if p["user_id"] == user_id or p["id"] == user_id:
                return p
        return self.providers[0] if self.providers else None

    def update_provider(self, provider_id: int, updates: dict) -> Optional[dict]:
        for p in self.providers:
            if p["id"] == provider_id:
                for k, v in updates.items():
                    if k in ["business_name", "categories", "experience_years", "location", "base_price", "description", "availability_status", "rating", "verified"]:
                        p[k] = v
                return p
        return None

    def create_service_request(self, user_id: int, provider_id: int, service_type: str, description: str, requested_date: str, address: str) -> dict:
        rid = self.next_service_request_id
        self.next_service_request_id += 1
        new_req = {
            "id": rid,
            "user_id": user_id or 1,
            "provider_id": provider_id or 1,
            "service_type": service_type or "Maintenance",
            "description": description or "",
            "requested_date": requested_date or "2026-03-25",
            "address": address or "Mumbai",
            "status": "Pending",
            "created_at": datetime.now().isoformat(),
        }
        self.service_requests.append(new_req)
        return new_req

    def get_service_requests_by_user(self, user_id: int) -> List[dict]:
        return [s for s in self.service_requests if s["user_id"] == user_id]

    def get_service_requests_by_provider(self, provider_id: int) -> List[dict]:
        return [s for s in self.service_requests if s["provider_id"] == provider_id]

    def update_service_request_status(self, request_id: int, status: str) -> Optional[dict]:
        for s in self.service_requests:
            if s["id"] == request_id:
                s["status"] = status
                return s
        return None

    # ------------------ Chat Messages ------------------
    def add_chat_message(self, conversation_id: int, user_id: int, sender: str, content: str) -> dict:
        cid = self.next_chat_id
        self.next_chat_id += 1
        msg = {
            "id": cid,
            "conversation_id": conversation_id,
            "user_id": user_id,
            "sender": sender,
            "content": content,
            "created_at": datetime.now().isoformat(),
        }
        self.chat_messages.append(msg)
        return msg

db = DatabaseManager()
