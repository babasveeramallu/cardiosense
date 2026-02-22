from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from datetime import datetime
from risk_engine import calculate_risk
from llm_service import get_explanation
from database import init_db, save_reading, get_all_readings, get_summary_report, clear_all_readings
from pdf_generator import generate_pdf_report

app = FastAPI()

# Initialize database on startup
init_db()

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
    p_wave_duration: float = 0.08  # Normal: 0.06-0.11 seconds
    pr_interval: float = 0.16  # Normal: 0.12-0.20 seconds
    qrs_duration: float = 0.09  # Normal: 0.06-0.10 seconds
    qt_interval: float = 0.40  # Normal: 0.36-0.44 seconds
    t_wave_amplitude: float = 0.3  # Normal: 0.1-0.5 mV
    st_segment_elevation: float = 0.0  # Normal: -0.05 to 0.1 mV

@app.get("/")
def root():
    return {"status": "CardioSense API running"}

@app.post("/analyze")
def analyze_vitals(vitals: VitalSigns):
    risk_score, risk_level = calculate_risk(vitals)
    explanation = get_explanation(vitals, risk_score, risk_level)
    
    # Check if 911 should be called
    emergency_alert = None
    if risk_level == "CRITICAL":
        emergency_alert = {
            "call_911": True,
            "reason": "Critical cardiac event detected",
            "priority": "IMMEDIATE"
        }
    
    # Save to database
    save_reading(vitals, risk_score, risk_level, explanation)
    
    response = {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "explanation": explanation,
        "vitals": vitals.model_dump()
    }
    
    if emergency_alert:
        response["emergency_alert"] = emergency_alert
    
    return response

@app.get("/history")
def get_history():
    return get_all_readings()

@app.get("/report")
def get_report():
    return get_summary_report()

@app.get("/report/pdf")
def get_pdf_report(patient_name: str = "John Doe", patient_age: int = 45):
    report = get_summary_report()
    pdf_buffer = generate_pdf_report(report, patient_name, patient_age)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=cardiosense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"}
    )

@app.delete("/clear")
def clear_history():
    clear_all_readings()
    return {"message": "All readings cleared"}
