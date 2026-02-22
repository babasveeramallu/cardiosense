import requests
import time
import random

API_URL = "http://localhost:8000"

def scenario_critical_heart_attack():
    print("\n" + "="*70)
    print("SCENARIO 3: CRITICAL - HEART ATTACK PROGRESSION → 911 EMERGENCY")
    print("="*70 + "\n")
    
    for i in range(5):
        progress = i / 5.0
        
        vitals = {
            "heart_rate": int(75 + progress * 85),
            "blood_pressure_systolic": int(125 + progress * 70),
            "blood_pressure_diastolic": int(78 + progress * 50),
            "oxygen_saturation": int(98 - progress * 15),
            "temperature": round(37.0 + progress * 1.5, 1),
            "p_wave_duration": round(0.08 + progress * 0.06, 2),
            "pr_interval": round(0.16 + progress * 0.08, 2),
            "qrs_duration": round(0.08 + progress * 0.06, 2),
            "qt_interval": round(0.40 + progress * 0.15, 2),
            "t_wave_amplitude": round(0.30 - progress * 0.50, 2),
            "st_segment_elevation": round(0.0 + progress * 0.25, 2)
        }
        
        response = requests.post(f"{API_URL}/analyze", json=vitals)
        if response.status_code == 200:
            data = response.json()
            print(f"Reading {i+1}/5 - Risk: {data['risk_level']} (Score: {data['risk_score']})")
            print(f"  HR: {vitals['heart_rate']} | BP: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']} | SpO2: {vitals['oxygen_saturation']}%")
            print(f"  ECG: ST={vitals['st_segment_elevation']}mV (STEMI if >0.1)")
            
            if 'emergency_alert' in data:
                print(f"\n  🚨🚨🚨 EMERGENCY: CALLING 911 NOW 🚨🚨🚨\n")
            elif data['risk_level'] == 'HIGH':
                print(f"  🔴 HIGH RISK")
            print()
        
        time.sleep(0.1)
    
    print("🚨 Scenario 3 Complete: CRITICAL EVENT - 911 CALLED\n")

if __name__ == "__main__":
    scenario_critical_heart_attack()
