import ollama
import sys
sys.path.append('../rag_pipeline')
from rag_query import query_medical_knowledge

def get_explanation(vitals, risk_score, risk_level):
    # Get relevant medical context from RAG
    context = query_medical_knowledge(vitals, risk_level)
    
    # Build prompt for Llama
    prompt = f"""You are a medical AI assistant. Analyze these vital signs and provide a brief explanation.

Vital Signs:
- Heart Rate: {vitals.heart_rate} bpm
- Blood Pressure: {vitals.blood_pressure_systolic}/{vitals.blood_pressure_diastolic} mmHg
- Oxygen Saturation: {vitals.oxygen_saturation}%
- Temperature: {vitals.temperature}°C

Risk Assessment: {risk_level} (Score: {risk_score})

Medical Context:
{context}

Provide a concise 2-3 sentence explanation of the cardiac risk and any immediate concerns."""

    try:
        response = ollama.generate(model='llama3.2:3b', prompt=prompt)
        return response['response']
    except Exception as e:
        return f"Risk level: {risk_level}. Unable to generate detailed explanation."
