import requests
import time
import random

API_URL = "http://localhost:8000"

def scenario_normal():
    print("\n" + "="*70)
    print("SCENARIO 1: NORMAL VITALS - Healthy Patient")
    print("="*70 + "\n")
    
    for i in range(5):
        vitals = {
            "heart_rate": random.randint(65, 80),
            "blood_pressure_systolic": random.randint(110, 125),
            "blood_pressure_diastolic": random.randint(70, 80),
            "oxygen_saturation": random.randint(97, 100),
            "temperature": round(random.uniform(36.5, 37.2), 1),
            "p_wave_duration": round(random.uniform(0.07, 0.10), 2),
            "pr_interval": round(random.uniform(0.14, 0.18), 2),
            "qrs_duration": round(random.uniform(0.07, 0.09), 2),
            "qt_interval": round(random.uniform(0.38, 0.42), 2),
            "t_wave_amplitude": round(random.uniform(0.2, 0.4), 2),
            "st_segment_elevation": round(random.uniform(-0.02, 0.05), 2)
        }
        
        response = requests.post(f"{API_URL}/analyze", json=vitals)
        if response.status_code == 200:
            data = response.json()
            print(f"Reading {i+1}/5 - Risk: {data['risk_level']} (Score: {data['risk_score']})")
            print(f"  HR: {vitals['heart_rate']} | BP: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']} | SpO2: {vitals['oxygen_saturation']}%\n")
        
        time.sleep(0.1)
    
    print("✅ Scenario 1 Complete: Patient stable\n")

if __name__ == "__main__":
    scenario_normal()
