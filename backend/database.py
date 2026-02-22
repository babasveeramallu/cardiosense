import sqlite3
from datetime import datetime
import json

DB_PATH = "cardiosense.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            heart_rate INTEGER,
            blood_pressure_systolic INTEGER,
            blood_pressure_diastolic INTEGER,
            oxygen_saturation INTEGER,
            temperature REAL,
            risk_score INTEGER,
            risk_level TEXT,
            explanation TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_reading(vitals, risk_score, risk_level, explanation):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO readings 
        (timestamp, heart_rate, blood_pressure_systolic, blood_pressure_diastolic, 
         oxygen_saturation, temperature, risk_score, risk_level, explanation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        vitals.heart_rate,
        vitals.blood_pressure_systolic,
        vitals.blood_pressure_diastolic,
        vitals.oxygen_saturation,
        vitals.temperature,
        risk_score,
        risk_level,
        explanation
    ))
    conn.commit()
    conn.close()

def get_all_readings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM readings ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    
    readings = []
    for row in rows:
        readings.append({
            "id": row[0],
            "timestamp": row[1],
            "heart_rate": row[2],
            "blood_pressure_systolic": row[3],
            "blood_pressure_diastolic": row[4],
            "oxygen_saturation": row[5],
            "temperature": row[6],
            "risk_score": row[7],
            "risk_level": row[8],
            "explanation": row[9]
        })
    return readings

def get_summary_report():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM readings")
    total_readings = cursor.fetchone()[0]
    
    if total_readings == 0:
        return {"message": "No readings recorded"}
    
    cursor.execute("""
        SELECT 
            AVG(heart_rate) as avg_hr,
            AVG(blood_pressure_systolic) as avg_bp_sys,
            AVG(blood_pressure_diastolic) as avg_bp_dia,
            AVG(oxygen_saturation) as avg_spo2,
            AVG(temperature) as avg_temp,
            AVG(risk_score) as avg_risk
        FROM readings
    """)
    averages = cursor.fetchone()
    
    cursor.execute("SELECT risk_level, COUNT(*) FROM readings GROUP BY risk_level")
    risk_distribution = dict(cursor.fetchall())
    
    cursor.execute("SELECT MAX(risk_score), timestamp FROM readings")
    max_risk = cursor.fetchone()
    
    conn.close()
    
    return {
        "total_readings": total_readings,
        "averages": {
            "heart_rate": round(averages[0], 1),
            "blood_pressure": f"{round(averages[1], 1)}/{round(averages[2], 1)}",
            "oxygen_saturation": round(averages[3], 1),
            "temperature": round(averages[4], 1),
            "risk_score": round(averages[5], 1)
        },
        "risk_distribution": risk_distribution,
        "highest_risk": {
            "score": max_risk[0],
            "timestamp": max_risk[1]
        }
    }

def clear_all_readings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM readings")
    conn.commit()
    conn.close()
