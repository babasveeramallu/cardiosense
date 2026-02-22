import pytest
from fastapi.testclient import TestClient
import sys
sys.path.append('../backend')
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "CardioSense API running"

def test_analyze_normal_vitals():
    vitals = {
        "heart_rate": 75,
        "blood_pressure_systolic": 120,
        "blood_pressure_diastolic": 80,
        "oxygen_saturation": 98,
        "temperature": 37.0
    }
    response = client.post("/analyze", json=vitals)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "risk_level" in data
    assert data["risk_level"] == "LOW"

def test_analyze_high_risk():
    vitals = {
        "heart_rate": 130,
        "blood_pressure_systolic": 190,
        "blood_pressure_diastolic": 125,
        "oxygen_saturation": 88,
        "temperature": 38.5
    }
    response = client.post("/analyze", json=vitals)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] in ["HIGH", "CRITICAL"]

def test_analyze_moderate_risk():
    vitals = {
        "heart_rate": 105,
        "blood_pressure_systolic": 145,
        "blood_pressure_diastolic": 92,
        "oxygen_saturation": 94,
        "temperature": 37.2
    }
    response = client.post("/analyze", json=vitals)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] in ["MODERATE", "HIGH"]

def test_invalid_vitals():
    vitals = {
        "heart_rate": "invalid",
        "blood_pressure_systolic": 120,
        "blood_pressure_diastolic": 80,
        "oxygen_saturation": 98,
        "temperature": 37.0
    }
    response = client.post("/analyze", json=vitals)
    assert response.status_code == 422
