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
    temperature: 37.0,
    p_wave_duration: 0.08,
    pr_interval: 0.16,
    qrs_duration: 0.09,
    qt_interval: 0.40,
    t_wave_amplitude: 0.3,
    st_segment_elevation: 0.0
  });
  
  const [analysis, setAnalysis] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [liveMode, setLiveMode] = useState(false);
  const [patientName, setPatientName] = useState('John Doe');
  const [patientAge, setPatientAge] = useState(45);

  // Auto-refresh latest reading every 2 seconds in live mode
  useEffect(() => {
    if (!liveMode) return;
    
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_URL}/history`);
        const data = await response.json();
        
        if (data.length > 0) {
          const latest = data[0];
          
          // Update vitals with latest reading
          setVitals({
            heart_rate: latest.heart_rate,
            blood_pressure_systolic: latest.blood_pressure_systolic,
            blood_pressure_diastolic: latest.blood_pressure_diastolic,
            oxygen_saturation: latest.oxygen_saturation,
            temperature: latest.temperature,
            p_wave_duration: 0.08 + (latest.risk_score * 0.01),
            pr_interval: 0.16 + (latest.risk_score * 0.01),
            qrs_duration: 0.09 + (latest.risk_score * 0.005),
            qt_interval: 0.40 + (latest.risk_score * 0.01),
            t_wave_amplitude: 0.3 - (latest.risk_score * 0.02),
            st_segment_elevation: (latest.risk_score > 10 ? 0.15 : 0.0)
          });
          
          // Update analysis
          setAnalysis({
            risk_score: latest.risk_score,
            risk_level: latest.risk_level,
            explanation: latest.explanation,
            emergency_alert: latest.risk_level === 'CRITICAL' ? {
              call_911: true,
              reason: 'Critical cardiac event detected',
              priority: 'IMMEDIATE'
            } : null
          });
          
          // Update history for charts
          const historyData = data.slice(0, 20).reverse().map(r => ({
            time: new Date(r.timestamp).toLocaleTimeString(),
            hr: r.heart_rate,
            bp: r.blood_pressure_systolic,
            spo2: r.oxygen_saturation,
            risk: r.risk_score,
            st: 0,
            t_wave: 0.3
          }));
          setHistory(historyData);
        }
      } catch (error) {
        console.error('Error fetching live data:', error);
      }
    }, 2000);
    
    return () => clearInterval(interval);
  }, [liveMode]);

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
        risk: data.risk_score,
        st: vitals.st_segment_elevation,
        t_wave: vitals.t_wave_amplitude
      }]);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  const generateECGWaveform = () => {
    const points = [];
    const baseY = 50;
    
    for (let x = 0; x < 100; x++) {
      let y = baseY;
      
      // P wave (atrial depolarization)
      if (x >= 10 && x <= 20) {
        y = baseY - (vitals.p_wave_duration * 50) * Math.sin((x - 10) * Math.PI / 10);
      }
      // PR segment
      else if (x > 20 && x < 30) {
        y = baseY;
      }
      // QRS complex (ventricular depolarization)
      else if (x >= 30 && x <= 40) {
        if (x < 35) {
          y = baseY + 10; // Q wave
        } else if (x < 38) {
          y = baseY - (vitals.qrs_duration * 200); // R wave (tall spike)
        } else {
          y = baseY + 5; // S wave
        }
      }
      // ST segment (critical for heart attack detection)
      else if (x > 40 && x < 55) {
        y = baseY + (vitals.st_segment_elevation * 100); // Elevation = heart attack
      }
      // T wave (repolarization)
      else if (x >= 55 && x <= 75) {
        y = baseY - (vitals.t_wave_amplitude * 80) * Math.sin((x - 55) * Math.PI / 20);
      }
      // Baseline
      else {
        y = baseY;
      }
      
      points.push({ x, y });
    }
    return points;
  };

  const ecgData = React.useMemo(() => generateECGWaveform(), [vitals.p_wave_duration, vitals.qrs_duration, vitals.st_segment_elevation, vitals.t_wave_amplitude]);

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
        <div className="live-toggle">
          <label>
            <input 
              type="checkbox" 
              checked={liveMode} 
              onChange={(e) => setLiveMode(e.target.checked)}
            />
            <span className={liveMode ? 'live-active' : ''}>
              {liveMode ? '🔴 LIVE' : '⚪ Manual Mode'}
            </span>
          </label>
        </div>
      </header>

      <div className="dashboard">
        <div className="vitals-input">
          <h2>Vital Signs Input</h2>
          <div className="input-grid">
            <div className="input-group">
              <label>Patient Name</label>
              <input
                type="text"
                value={patientName}
                onChange={(e) => setPatientName(e.target.value)}
              />
            </div>
            <div className="input-group">
              <label>Patient Age</label>
              <input
                type="number"
                value={patientAge}
                onChange={(e) => setPatientAge(parseInt(e.target.value))}
              />
            </div>
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
            <div className="input-group">
              <label>ST Elevation (mV)</label>
              <input
                type="number"
                step="0.01"
                value={vitals.st_segment_elevation}
                onChange={(e) => setVitals({...vitals, st_segment_elevation: parseFloat(e.target.value)})}
              />
            </div>
            <div className="input-group">
              <label>T Wave (mV)</label>
              <input
                type="number"
                step="0.01"
                value={vitals.t_wave_amplitude}
                onChange={(e) => setVitals({...vitals, t_wave_amplitude: parseFloat(e.target.value)})}
              />
            </div>
          </div>
          <button onClick={analyzeVitals} disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Risk'}
          </button>
          <button onClick={async () => {
            window.open(`${API_URL}/report/pdf?patient_name=${encodeURIComponent(patientName)}&patient_age=${patientAge}`, '_blank');
          }} style={{marginTop: '1rem', background: '#10b981'}}>
            📄 Download PDF Report
          </button>
        </div>

        {analysis && (
          <div className="risk-display" style={{borderColor: getRiskColor(analysis.risk_level)}}>
            <h2>Risk Assessment</h2>
            <div className="risk-level" style={{color: getRiskColor(analysis.risk_level)}}>
              {analysis.risk_level}
            </div>
            <div className="risk-score">Score: {analysis.risk_score}</div>
            {analysis.emergency_alert && (
              <div className="emergency-alert">
                🚨 EMERGENCY: {analysis.emergency_alert.reason} - CALLING 911 NOW!
              </div>
            )}
            <div className="explanation">
              {analysis.explanation.split('.').filter(s => s.trim()).map((sentence, i) => (
                <div key={i} className="bullet-point">• {sentence.trim()}.</div>
              ))}
            </div>
          </div>
        )}

        <div className="ecg-container">
          <h2>ECG Waveform</h2>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={ecgData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="x" hide />
              <YAxis domain={[0, 100]} hide />
              <Line type="monotone" dataKey="y" stroke="#10b981" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
          <div className="ecg-labels">
            <span>P: {vitals.p_wave_duration}s</span>
            <span>PR: {vitals.pr_interval}s</span>
            <span>QRS: {vitals.qrs_duration}s</span>
            <span>QT: {vitals.qt_interval}s</span>
            <span>ST: {vitals.st_segment_elevation}mV</span>
            <span>T: {vitals.t_wave_amplitude}mV</span>
          </div>
        </div>

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
