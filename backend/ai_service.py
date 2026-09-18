import httpx
import json
from typing import Optional, Dict, Any
from backend.config import settings

SYSTEM_PROMPT = """You are UrjaExpert AI, an advanced energy consultant and sustainability engineer specializing in Indian household energy efficiency, rooftop solar PV feasibility, DISCOM electricity tariffs, BEE 5-star appliance selection, and carbon footprint reduction.

Your core competencies include:
1. Indian DISCOM tariffs: Slab rates, fixed charges, power factor, fuel adjustment charges (FAC/FPPCA), and time-of-day (ToD) tariffs across states like Maharashtra (MSEDCL, Adani, Tata Power), Delhi (BSES, TPDDL), Karnataka (BESCOM), Tamil Nadu (TANGEDCO), Gujarat (UGVCL, DGVCL), Uttar Pradesh (UPPCL), Rajasthan (JVVNL), etc.
2. Rooftop Solar & Subsidies: PM Surya Ghar Muft Bijli Yojana (central subsidy of ₹30,000 for 1kW, ₹60,000 for 2kW, ₹78,000 for 3kW+), net metering regulations, payback periods (typically 3-4 years in India), and solar generation factors (~4-5 kWh/day per kWp).
3. Appliance Energy Efficiency: BEE star rating analysis, ISEER ratings for inverter ACs, BLDC motor ceiling fans (saving 50-60% power vs conventional fans), inverter refrigerators, heat-pump water heaters, and induction cooktops.
4. Actionable Indian Household Advice: Providing specific monetary savings in INR (₹) and kWh, optimal temperature setpoints (24-26°C for ACs), and proactive peak-shaving tips.

Keep your tone helpful, professional, structured, and easy to read with bullet points and clear numbers."""

def generate_local_expert_response(prompt: str) -> str:
    """High-quality domain-expert response generator when Mistral API key is not configured."""
    p_lower = prompt.lower()

    if any(k in p_lower for k in ["solar", "rooftop", "sun", "panel", "pv", "subsidy", "pm surya"]):
        return (
            "### Rooftop Solar Feasibility & PM Surya Ghar Subsidy Guide\n\n"
            "Installing rooftop solar is currently one of the highest-yield home investments in India:\n\n"
            "**1. PM Surya Ghar Muft Bijli Yojana Subsidies:**\n"
            "- **1 kW System:** Central financial assistance of **₹30,000** (ideal for monthly usage ~120-150 units).\n"
            "- **2 kW System:** Central financial assistance of **₹60,000** (ideal for monthly usage ~250-300 units).\n"
            "- **3 kW+ System:** Flat maximum subsidy of **₹78,000** (covers 300-450+ units/month).\n\n"
            "**2. Generation & Savings:**\n"
            "- A **3 kW rooftop system** produces approximately **12 to 15 kWh (units) daily**, totaling ~4,500 kWh annually.\n"
            "- At an average Indian grid slab rate of ₹7.50/kWh, this saves approximately **₹33,750 per year** on electricity bills.\n\n"
            "**3. Return on Investment (ROI) & Payback:**\n"
            "- Benchmark turnkey cost: ~₹1,80,000 for 3 kW.\n"
            "- Net cost after subsidy: ~₹1,02,000.\n"
            "- **Payback period:** Approx. **3.0 to 3.5 years**, followed by 20+ years of virtually free solar power with a 25-year panel warranty."
        )

    if any(k in p_lower for k in ["bill", "analyzer", "tariff", "msedcl", "bescom", "tangedco", "uppcl", "adani", "bses"]):
        return (
            "### Electricity Bill Breakdown & Tariff Optimization\n\n"
            "Indian residential electricity tariffs follow an escalating progressive slab structure:\n\n"
            "**1. Key Bill Components:**\n"
            "- **Energy Charges (Slabs):** Typically ₹3.50/unit for 0-100 units, stepping up to ₹7.50-₹9.00/unit for 101-300 units, and ₹11.00-₹14.00/unit above 300 units.\n"
            "- **Fixed Demand Charges:** ₹100 - ₹350/month based on your sanctioned connected load (kW).\n"
            "- **FPPCA / Fuel Surcharge:** A variable monthly pass-through cost (5-15% of energy charges).\n"
            "- **Electricity Duty & Tax:** State-levied duty ranging from 5% to 16%.\n\n"
            "**2. Immediate Action Steps to Lower Your Bill:**\n"
            "- Maintain total consumption within the lower slab (below 300 units) to avoid exponential top-slab penalties.\n"
            "- Review your sanctioned load: If your peak demand never crosses 2.5 kW, lowering sanctioned load from 5 kW to 3 kW saves ₹150-₹300 monthly in fixed charges."
        )

    if any(k in p_lower for k in ["ac", "air conditioner", "cooling", "inverter", "iseer"]):
        return (
            "### Air Conditioning Energy Optimization & Inverter Sizing\n\n"
            "Air conditioners typically account for 55% to 70% of peak summer electricity bills in Indian homes:\n\n"
            "**1. The 24°C Rule (BEE Guideline):**\n"
            "- Setting your thermostat to **24°C instead of 18°C saves 24% to 36% electricity** (each 1°C increase saves approx. 6% power).\n\n"
            "**2. ISEER Rating Impact:**\n"
            "- A **5-Star Inverter AC** (ISEER > 5.0) consumes ~550-650 kWh annually compared to ~1,000+ kWh for an older non-inverter 3-star AC.\n"
            "- Annual savings: ~₹3,500 to ₹4,500 per year at ₹8/kWh.\n\n"
            "**3. Maintenance Checklist:**\n"
            "- Clean air filters every 15 days (a clogged filter increases compressor load by 15%).\n"
            "- Ensure annual condenser coil chemical wash to sustain heat dissipation efficiency."
        )

    if any(k in p_lower for k in ["fan", "bldc", "refrigerator", "fridge", "appliance", "buy", "before you buy"]):
        return (
            "### Smart Appliance Buying Guide & BLDC Savings\n\n"
            "**1. BLDC Ceiling Fans:**\n"
            "- Conventional induction fans consume **75W to 80W**.\n"
            "- Modern BLDC fans consume only **28W to 32W** at full speed, saving ~60% electricity.\n"
            "- Operating 12 hours/day saves ~200 kWh per fan annually (~₹1,500/year per fan). The price difference is recovered in under 14 months!\n\n"
            "**2. Inverter Frost-Free Refrigerators:**\n"
            "- Variable-speed compressors adjust speed based on internal temperature rather than cycling on/off.\n"
            "- Look for BEE 5-Star rated models with Annual Energy Consumption under 200 kWh/year."
        )

    return (
        "### UrjaExpert AI Energy Recommendations\n\n"
        f"Thank you for your question: *'{prompt}'*\n\n"
        "Here are three high-impact steps to reduce household electricity costs:\n\n"
        "1. **Baseline Energy Auditing:** Log daily meter readings in the Energy Forecasting module to detect phantom standby loads and unoptimized evening peaks.\n"
        "2. **Appliance Modernization:** Prioritize transitioning high-usage appliances (fans to BLDC, ACs to BEE 5-star dual inverter) for the fastest ROI.\n"
        "3. **Solar PV Adoption:** Leverage the **PM Surya Ghar** national subsidy (up to ₹78,000) to offset daytime air-conditioning and refrigeration loads directly from rooftop sunlight.\n\n"
        "Feel free to ask about specific DISCOM tariffs, solar sizing for your home square footage, or appliance payback calculations!"
    )

async def ask_mistral_ai(prompt: str) -> str:
    """
    Calls Mistral AI API using httpx if MISTRAL_API_KEY is configured.
    Falls back gracefully to rich domain-expert energy intelligence.
    """
    api_key = settings.MISTRAL_API_KEY.strip()
    if not api_key:
        return generate_local_expert_response(prompt)

    try:
        async with httpx.AsyncClient(timeout=25.0) as client:
            resp = await client.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "mistral-small-latest",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1000,
                },
            )
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices and "message" in choices[0]:
                    return choices[0]["message"].get("content", "").strip()
            # If rate limited or error, use domain-expert fallback
            return generate_local_expert_response(prompt)
    except Exception as e:
        print(f"[Mistral AI Error] {e}. Falling back to domain knowledge.")
        return generate_local_expert_response(prompt)
