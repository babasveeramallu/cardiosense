import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

const API_URL = 'http://192.168.12.195:8000';

function App() {
  const [vitals, setVitals] = useState({
    heart_rate: 75,
    blood_pressure_systolic: 120,
    blood_pressure_diastolic: 80,
    oxygen_saturation: 98,
    temperature: 37.0
  });
  
  const [analysis, setAnalysis] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const analyzeVitals = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(vitals)
      });
      const data = await response.json();
      setAnalysis(data);
      
      setHistory(prev => [...prev.slice(-19), {
        time: new Date().toLocaleTimeString(),
        hr: vitals.heart_rate,
        bp: vitals.blood_pressure_systolic,
        spo2: vitals.oxygen_saturation,
        risk: data.risk_score
      }]);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  const getRiskColor = (level) => {
    const colors = {
      LOW: '#10b981',
      MODERATE: '#f59e0b',
      HIGH: '#ef4444',
      CRITICAL: '#dc2626'
    };
    return colors[level] || '#6b7280';
  };

  return (
    <div className="app">
      <header>
        <h1>CardioSense AI</h1>
        <p>Real-time Cardiac Risk Monitoring</p>
      </header>

      <div className="dashboard">
        <div className="vitals-input">
          <h2>Vital Signs Input</h2>
          <div className="input-grid">
            <div className="input-group">
              <label>Heart Rate (bpm)</label>
              <input
                type="number"
                value={vitals.heart_rate}
                onChange={(e) => setVitals({...vitals, heart_rate: parseInt(e.target.value)})}
              />
            </div>
            <div className="input-group">
              <label>BP Systolic (mmHg)</label>
              <input
                type="number"
                value={vitals.blood_pressure_systolic}
                onChange={(e) => setVitals({...vitals, blood_pressure_systolic: parseInt(e.target.value)})}
              />
            </div>
            <div className="input-group">
              <label>BP Diastolic (mmHg)</label>
              <input
                type="number"
                value={vitals.blood_pressure_diastolic}
                onChange={(e) => setVitals({...vitals, blood_pressure_diastolic: parseInt(e.target.value)})}
              />
            </div>
            <div className="input-group">
              <label>SpO2 (%)</label>
              <input
                type="number"
                value={vitals.oxygen_saturation}
                onChange={(e) => setVitals({...vitals, oxygen_saturation: parseInt(e.target.value)})}
              />
            </div>
            <div className="input-group">
              <label>Temperature (°C)</label>
              <input
                type="number"
                step="0.1"
                value={vitals.temperature}
                onChange={(e) => setVitals({...vitals, temperature: parseFloat(e.target.value)})}
              />
            </div>
          </div>
          <button onClick={analyzeVitals} disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Risk'}
          </button>
        </div>

        {analysis && (
          <div className="risk-display" style={{borderColor: getRiskColor(analysis.risk_level)}}>
            <h2>Risk Assessment</h2>
            <div className="risk-level" style={{color: getRiskColor(analysis.risk_level)}}>
              {analysis.risk_level}
            </div>
            <div className="risk-score">Score: {analysis.risk_score}</div>
            <div className="explanation">{analysis.explanation}</div>
          </div>
        )}

        {history.length > 0 && (
          <div className="chart-container">
            <h2>Vital Signs History</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="time" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip contentStyle={{backgroundColor: '#1f2937', border: 'none'}} />
                <Legend />
                <Line type="monotone" dataKey="hr" stroke="#3b82f6" name="Heart Rate" />
                <Line type="monotone" dataKey="bp" stroke="#ef4444" name="BP Systolic" />
                <Line type="monotone" dataKey="spo2" stroke="#10b981" name="SpO2" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
