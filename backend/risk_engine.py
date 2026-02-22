def calculate_risk(vitals):
    score = 0
    
    # Heart rate scoring
    if vitals.heart_rate < 60 or vitals.heart_rate > 100:
        score += 2
    if vitals.heart_rate > 120:
        score += 3
    
    # Blood pressure scoring
    if vitals.blood_pressure_systolic > 140 or vitals.blood_pressure_diastolic > 90:
        score += 3
    if vitals.blood_pressure_systolic > 180 or vitals.blood_pressure_diastolic > 120:
        score += 5
    
    # Oxygen saturation scoring
    if vitals.oxygen_saturation < 95:
        score += 2
    if vitals.oxygen_saturation < 90:
        score += 4
    
    # Temperature scoring
    if vitals.temperature > 38.0 or vitals.temperature < 36.0:
        score += 2
    
    # Determine risk level
    if score >= 8:
        risk_level = "CRITICAL"
    elif score >= 5:
        risk_level = "HIGH"
    elif score >= 3:
        risk_level = "MODERATE"
    else:
        risk_level = "LOW"
    
    return score, risk_level
