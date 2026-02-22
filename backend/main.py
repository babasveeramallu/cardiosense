from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from risk_engine import calculate_risk
from llm_service import get_explanation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VitalSigns(BaseModel):
    heart_rate: int
    blood_pressure_systolic: int
    blood_pressure_diastolic: int
    oxygen_saturation: int
    temperature: float

@app.get("/")
def root():
    return {"status": "CardioSense API running"}

@app.post("/analyze")
def analyze_vitals(vitals: VitalSigns):
    risk_score, risk_level = calculate_risk(vitals)
    explanation = get_explanation(vitals, risk_score, risk_level)
    
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "explanation": explanation,
        "vitals": vitals.dict()
    }
