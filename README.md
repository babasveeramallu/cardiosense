# CardioSense AI

Real-time cardiac risk monitoring system using FastAPI, ChromaDB, Llama 3.2, and React.

## Features

- ✅ Real-time vital signs monitoring (HR, BP, SpO2, Temperature)
- ✅ ECG waveform analysis (P, QRS, ST, T waves)
- ✅ AI-powered risk assessment with Llama 3.2:3b
- ✅ Medical RAG pipeline with ChromaDB
- ✅ Live dashboard with auto-refresh
- ✅ Automatic 911 alerts for critical events
- ✅ PDF report generation with charts and ECG
- ✅ Complete test suite with 3 progressive scenarios

## Quick Start

### Prerequisites
- Raspberry Pi 5 (or any Linux/macOS system)
- Python 3.10+
- Node.js 18+
- Ollama with llama3.2:3b model

### Installation

```bash
# Clone repository
git clone https://github.com/babaveeramallu/cardiosense
cd cardiosense

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Initialize medical knowledge base
cd rag_pipeline
python3 rag_init.py
cd ..

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Running

**Terminal 1 - Backend:**
```bash
cd cardiosense
source venv/bin/activate
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd cardiosense/frontend
npm run dev
```

**Terminal 3 - Test Scenarios (Optional):**
```bash
cd cardiosense
source venv/bin/activate
cd tests
python3 test_scenarios.py
```

### Access

- **Dashboard**: http://localhost:5173 (or http://<PI_IP>:5173)
- **API Docs**: http://localhost:8000/docs
- **Backend API**: http://localhost:8000

## Usage

### Manual Mode
1. Open dashboard in browser
2. Enter patient name and age
3. Input vital signs and ECG parameters
4. Click "Analyze Risk"
5. View risk assessment and AI explanation
6. Download PDF report

### Live Mode
1. Toggle "LIVE" mode in dashboard
2. Run test scenarios in terminal
3. Watch dashboard auto-update every 2 seconds
4. See real-time ECG waveform changes
5. Get 911 alerts for critical events

## Testing

### Run API Tests
```bash
cd tests
pytest test_api.py -v
```

### Run Progressive Scenarios
```bash
cd tests
python3 test_scenarios.py
```

Scenarios:
1. **Normal**: 10 readings with healthy vitals
2. **Escalating to Moderate**: 15 readings showing cardiac stress
3. **Critical Heart Attack**: 20 readings progressing to STEMI with 911 alert

## API Endpoints

- `POST /analyze` - Analyze vitals and return risk assessment
- `GET /history` - Get all stored readings
- `GET /report` - Get summary statistics (JSON)
- `GET /report/pdf` - Download PDF report
- `DELETE /clear` - Clear all readings

## Architecture

- **Backend**: FastAPI with SQLite database
- **RAG**: ChromaDB with sentence-transformers embeddings
- **LLM**: Ollama with Llama 3.2:3b (local inference)
- **Frontend**: React + Vite + Recharts
- **Hardware**: Raspberry Pi 5 (all processing on-device)

## Project Structure

See [STRUCTURE.md](STRUCTURE.md) for detailed project organization.

## License

MIT License - see [LICENSE](LICENSE) file.
