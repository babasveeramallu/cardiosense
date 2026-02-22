import requests
import time
import random

API_URL = "http://localhost:8000"

def scenario_escalating_moderate():
    print("\n" + "="*70)
    print("SCENARIO 2: ESCALATING TO MODERATE - Cardiac Stress Developing")
    print("="*70 + "\n")
    
    for i in range(15):
        progress = i / 15.0
        
        vitals = {
            "heart_rate": int(70 + progress * 45),
            "blood_pressure_systolic": int(120 + progress * 35),
            "blood_pressure_diastolic": int(75 + progress * 20),
            "oxygen_saturation": int(99 - progress * 6),
            "temperature": round(36.8 + progress * 1.0, 1),
            "p_wave_duration": round(0.08 + progress * 0.03, 2),
            "pr_interval": round(0.16 + progress * 0.03, 2),
            "qrs_duration": round(0.08 + progress * 0.02, 2),
            "qt_interval": round(0.40 + progress * 0.06, 2),
            "t_wave_amplitude": round(0.35 - progress * 0.20, 2),
            "st_segment_elevation": round(0.0 - progress * 0.08, 2)
        }
        
        response = requests.post(f"{API_URL}/analyze", json=vitals)
        if response.status_code == 200:
            data = response.json()
            print(f"Reading {i+1}/15 - Risk: {data['risk_level']} (Score: {data['risk_score']})")
            print(f"  HR: {vitals['heart_rate']} | BP: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']} | SpO2: {vitals['oxygen_saturation']}%")
            print(f"  ECG: ST={vitals['st_segment_elevation']}mV, T={vitals['t_wave_amplitude']}mV")
            
            if data['risk_level'] in ['MODERATE', 'HIGH']:
                print(f"  ⚠️  {data['risk_level']} RISK DETECTED")
            print()
        
        time.sleep(0.3)
    
    print("⚠️  Scenario 2 Complete: Patient showing cardiac stress - monitoring recommended\n")

if __name__ == "__main__":
    scenario_escalating_moderate()
