# CardioSense AI

Real-time cardiac risk monitoring system using FastAPI, ChromaDB, Llama 3.2, and React.

## Setup on Raspberry Pi 5

### 1. Clone Repository
```bash
cd ~
git clone <your-repo-url> cardiosense
cd cardiosense
```

### 2. Backend Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Initialize RAG Knowledge Base
```bash
cd rag_pipeline
python3 rag_init.py
cd ..
```

### 4. Start Backend Server
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Frontend Setup (separate terminal)
```bash
cd ~/cardiosense/frontend
npm install
npm run dev
```

### 6. Update Frontend API URL
Edit `frontend/src/App.jsx` and replace `192.168.1.100` with your Pi's IP address (find with `hostname -I`).

## Testing

### Run API Tests
```bash
cd tests
pytest test_api.py -v
```

### Run Simulator
```bash
cd tests
python3 simulator.py normal    # Normal vitals
python3 simulator.py high_risk # High risk scenario
python3 simulator.py critical  # Critical scenario
```

## Access

- Backend API: `http://<PI_IP>:8000`
- Frontend Dashboard: `http://<PI_IP>:5173`
- API Docs: `http://<PI_IP>:8000/docs`

## Architecture

- **Backend**: FastAPI server with risk calculation engine
- **RAG**: ChromaDB with medical knowledge base
- **LLM**: Ollama with Llama 3.2:3b for explanations
- **Frontend**: React dashboard with Recharts visualization
