import requests
import time
import random
import sys

API_URL = "http://localhost:8000"

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

def simulate(interval=5, scenario="normal", duration=None):
    print(f"Starting simulator in {scenario} mode...")
    print(f"Sending vitals every {interval} seconds")
    print(f"API endpoint: {API_URL}/analyze")
    if duration:
        print(f"Will run for {duration} seconds")
    print("Press Ctrl+C to stop and see report\n")
    
    start_time = time.time()
    count = 0
    
    try:
        while True:
            vitals = generate_vitals(scenario)
            
            try:
                response = requests.post(f"{API_URL}/analyze", json=vitals)
                if response.status_code == 200:
                    data = response.json()
                    count += 1
                    print(f"[{time.strftime('%H:%M:%S')}] Reading #{count} - Risk: {data['risk_level']} (Score: {data['risk_score']})")
                    print(f"  HR: {vitals['heart_rate']} | BP: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']} | SpO2: {vitals['oxygen_saturation']}% | Temp: {vitals['temperature']}°C\n")
                else:
                    print(f"Error: {response.status_code}")
            except Exception as e:
                print(f"Connection error: {e}")
            
            if duration and (time.time() - start_time) >= duration:
                break
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("SIMULATION STOPPED - GENERATING REPORT")
        print("="*60 + "\n")
    
    # Get and display report
    try:
        response = requests.get(f"{API_URL}/report")
        if response.status_code == 200:
            report = response.json()
            
            if "message" in report:
                print(report["message"])
            else:
                print(f"📊 SUMMARY REPORT")
                print(f"{'='*60}\n")
                print(f"Total Readings: {report['total_readings']}")
                print(f"Duration: {int(time.time() - start_time)} seconds\n")
                
                print(f"📈 AVERAGE VITALS:")
                print(f"  Heart Rate: {report['averages']['heart_rate']} bpm")
                print(f"  Blood Pressure: {report['averages']['blood_pressure']} mmHg")
                print(f"  Oxygen Saturation: {report['averages']['oxygen_saturation']}%")
                print(f"  Temperature: {report['averages']['temperature']}°C")
                print(f"  Average Risk Score: {report['averages']['risk_score']}\n")
                
                print(f"⚠️  RISK DISTRIBUTION:")
                for level, count in report['risk_distribution'].items():
                    percentage = (count / report['total_readings']) * 100
                    print(f"  {level}: {count} readings ({percentage:.1f}%)")
                
                print(f"\n🚨 HIGHEST RISK EVENT:")
                print(f"  Score: {report['highest_risk']['score']}")
                print(f"  Time: {report['highest_risk']['timestamp']}")
                
                print(f"\n{'='*60}")
                print(f"View full history at: {API_URL}/history")
                print(f"Clear data with: curl -X DELETE {API_URL}/clear")
                print(f"{'='*60}\n")
    except Exception as e:
        print(f"Error fetching report: {e}")

if __name__ == "__main__":
    scenario = sys.argv[1] if len(sys.argv) > 1 else "normal"
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else None
    simulate(scenario=scenario, duration=duration)
