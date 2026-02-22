import requests
import time
import random

API_URL = "http://localhost:8000/analyze"

def generate_vitals(scenario="normal"):
    if scenario == "normal":
        return {
            "heart_rate": random.randint(65, 85),
            "blood_pressure_systolic": random.randint(110, 130),
            "blood_pressure_diastolic": random.randint(70, 85),
            "oxygen_saturation": random.randint(96, 100),
            "temperature": round(random.uniform(36.5, 37.3), 1)
        }
    elif scenario == "high_risk":
        return {
            "heart_rate": random.randint(120, 140),
            "blood_pressure_systolic": random.randint(160, 190),
            "blood_pressure_diastolic": random.randint(100, 120),
            "oxygen_saturation": random.randint(88, 93),
            "temperature": round(random.uniform(37.8, 39.0), 1)
        }
    elif scenario == "critical":
        return {
            "heart_rate": random.randint(140, 160),
            "blood_pressure_systolic": random.randint(180, 200),
            "blood_pressure_diastolic": random.randint(120, 140),
            "oxygen_saturation": random.randint(85, 89),
            "temperature": round(random.uniform(38.5, 40.0), 1)
        }

def simulate(interval=5, scenario="normal"):
    print(f"Starting simulator in {scenario} mode...")
    print(f"Sending vitals every {interval} seconds")
    print(f"API endpoint: {API_URL}\n")
    
    while True:
        vitals = generate_vitals(scenario)
        
        try:
            response = requests.post(API_URL, json=vitals)
            if response.status_code == 200:
                data = response.json()
                print(f"[{time.strftime('%H:%M:%S')}] Risk: {data['risk_level']} (Score: {data['risk_score']})")
                print(f"  HR: {vitals['heart_rate']} | BP: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']} | SpO2: {vitals['oxygen_saturation']}% | Temp: {vitals['temperature']}°C")
                print(f"  {data['explanation'][:100]}...\n")
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Connection error: {e}")
        
        time.sleep(interval)

if __name__ == "__main__":
    import sys
    scenario = sys.argv[1] if len(sys.argv) > 1 else "normal"
    simulate(scenario=scenario)
