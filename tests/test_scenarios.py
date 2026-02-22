import requests
import time
import random

API_URL = "http://localhost:8000"

# Scenario 1: Normal vitals throughout
def scenario_normal():
    print("\n" + "="*70)
    print("SCENARIO 1: NORMAL VITALS - Healthy Patient")
    print("="*70 + "\n")
    
    for i in range(10):
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
            print(f"Reading {i+1}/10 - Risk: {data['risk_level']} (Score: {data['risk_score']})")
            print(f"  HR: {vitals['heart_rate']} | BP: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']} | SpO2: {vitals['oxygen_saturation']}%")
            print(f"  ECG: P={vitals['p_wave_duration']}s, QRS={vitals['qrs_duration']}s, T={vitals['t_wave_amplitude']}mV, ST={vitals['st_segment_elevation']}mV\n")
        
        time.sleep(0.5)
    
    print("✅ Scenario 1 Complete: Patient stable\n")

# Scenario 2: Normal → Moderate (developing cardiac stress)
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
            print(f"  ECG: P={vitals['p_wave_duration']}s, QRS={vitals['qrs_duration']}s, T={vitals['t_wave_amplitude']}mV, ST={vitals['st_segment_elevation']}mV")
            
            if data['risk_level'] in ['MODERATE', 'HIGH']:
                print(f"  ⚠️  {data['risk_level']} RISK DETECTED")
            print()
        
        time.sleep(0.5)
    
    print("⚠️  Scenario 2 Complete: Patient showing cardiac stress - monitoring recommended\n")

# Scenario 3: Normal → Critical (heart attack progression) → 911 CALL
def scenario_critical_heart_attack():
    print("\n" + "="*70)
    print("SCENARIO 3: CRITICAL - HEART ATTACK PROGRESSION → 911 EMERGENCY")
    print("="*70 + "\n")
    
    for i in range(20):
        progress = i / 20.0
        
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
            print(f"Reading {i+1}/20 - Risk: {data['risk_level']} (Score: {data['risk_score']})")
            print(f"  HR: {vitals['heart_rate']} | BP: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']} | SpO2: {vitals['oxygen_saturation']}%")
            print(f"  ECG: P={vitals['p_wave_duration']}s, QRS={vitals['qrs_duration']}s, T={vitals['t_wave_amplitude']}mV, ST={vitals['st_segment_elevation']}mV")
            
            if 'emergency_alert' in data:
                print(f"\n  🚨🚨🚨 EMERGENCY ALERT 🚨🚨🚨")
                print(f"  {data['emergency_alert']['reason']}")
                print(f"  Priority: {data['emergency_alert']['priority']}")
                print(f"  Action: CALLING 911 NOW")
                print(f"  🚨🚨🚨 EMERGENCY ALERT 🚨🚨🚨\n")
            elif data['risk_level'] == 'HIGH':
                print(f"  🔴 HIGH RISK - Approaching critical threshold")
            elif data['risk_level'] == 'MODERATE':
                print(f"  🟡 MODERATE RISK - Vitals deteriorating")
            print()
        
        time.sleep(0.5)
    
    print("🚨 Scenario 3 Complete: CRITICAL CARDIAC EVENT - 911 CALLED - EMERGENCY RESPONSE REQUIRED\n")

def run_all_scenarios():
    print("\n" + "="*70)
    print("CARDIOSENSE AI - COMPREHENSIVE CARDIAC MONITORING TEST")
    print("Testing 3 Progressive Scenarios with ECG Analysis")
    print("="*70)
    
    input("\nPress Enter to start Scenario 1 (Normal Vitals)...")
    scenario_normal()
    
    input("Press Enter to start Scenario 2 (Escalating to Moderate)...")
    scenario_escalating_moderate()
    
    input("Press Enter to start Scenario 3 (Critical Heart Attack → 911)...")
    scenario_critical_heart_attack()
    
    # Get final report
    print("\n" + "="*70)
    print("GENERATING COMPREHENSIVE REPORT")
    print("="*70 + "\n")
    
    response = requests.get(f"{API_URL}/report")
    if response.status_code == 200:
        report = response.json()
        print(f"📊 FINAL SUMMARY")
        print(f"Total Readings: {report['total_readings']}")
        print(f"\n📈 Average Vitals:")
        for key, value in report['averages'].items():
            print(f"  {key}: {value}")
        print(f"\n⚠️  Risk Distribution:")
        for level, count in report['risk_distribution'].items():
            print(f"  {level}: {count} readings")
        print(f"\n🚨 Highest Risk Event:")
        print(f"  Score: {report['highest_risk']['score']}")
        print(f"  Time: {report['highest_risk']['timestamp']}")
    
    print("\n" + "="*70)
    print("ALL SCENARIOS COMPLETE")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_all_scenarios()
