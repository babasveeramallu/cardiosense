def calculate_risk(vitals):
    score = 0
    cardiac_emergency = False
    
    # Heart rate scoring
    if vitals.heart_rate < 60 or vitals.heart_rate > 100:
        score += 2
    if vitals.heart_rate > 120:
        score += 3
    if vitals.heart_rate > 150:
        score += 5
        cardiac_emergency = True
    
    # Blood pressure scoring
    if vitals.blood_pressure_systolic > 140 or vitals.blood_pressure_diastolic > 90:
        score += 3
    if vitals.blood_pressure_systolic > 180 or vitals.blood_pressure_diastolic > 120:
        score += 5
        cardiac_emergency = True
    
    # Oxygen saturation scoring
    if vitals.oxygen_saturation < 95:
        score += 2
    if vitals.oxygen_saturation < 90:
        score += 4
    if vitals.oxygen_saturation < 85:
        score += 6
        cardiac_emergency = True
    
    # Temperature scoring
    if vitals.temperature > 38.0 or vitals.temperature < 36.0:
        score += 2
    
    # ECG Analysis - P Wave
    if vitals.p_wave_duration > 0.12:  # Prolonged P wave (atrial enlargement)
        score += 3
    if vitals.p_wave_duration < 0.06:  # Shortened P wave
        score += 2
    
    # PR Interval (AV conduction)
    if vitals.pr_interval > 0.20:  # First-degree AV block
        score += 4
        cardiac_emergency = True
    if vitals.pr_interval < 0.12:  # Pre-excitation syndrome
        score += 3
    
    # QRS Duration (ventricular conduction)
    if vitals.qrs_duration > 0.12:  # Bundle branch block
        score += 5
        cardiac_emergency = True
    
    # QT Interval (repolarization)
    if vitals.qt_interval > 0.50:  # Long QT syndrome - risk of sudden death
        score += 6
        cardiac_emergency = True
    if vitals.qt_interval < 0.30:  # Short QT syndrome
        score += 4
    
    # T Wave Analysis (ischemia indicator)
    if vitals.t_wave_amplitude < 0.1:  # Flattened T wave (ischemia)
        score += 4
    if vitals.t_wave_amplitude < 0:  # Inverted T wave (severe ischemia)
        score += 7
        cardiac_emergency = True
    if vitals.t_wave_amplitude > 0.6:  # Peaked T wave (hyperkalemia)
        score += 5
        cardiac_emergency = True
    
    # ST Segment (heart attack indicator)
    if vitals.st_segment_elevation > 0.1:  # ST elevation - STEMI (heart attack)
        score += 10
        cardiac_emergency = True
    if vitals.st_segment_elevation < -0.1:  # ST depression (ischemia)
        score += 6
        cardiac_emergency = True
    
    # Determine risk level
    if cardiac_emergency or score >= 15:
        risk_level = "CRITICAL"
    elif score >= 8:
        risk_level = "HIGH"
    elif score >= 3:
        risk_level = "MODERATE"
    else:
        risk_level = "LOW"
    
    return score, risk_level
