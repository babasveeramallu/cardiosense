# CardioSense AI - Project Structure

```
CardioSense/
│
├── backend/                    # FastAPI Backend
│   ├── main.py                # API endpoints and server
│   ├── risk_engine.py         # Cardiac risk scoring logic
│   ├── llm_service.py         # Ollama + RAG integration
│   ├── database.py            # SQLite database operations
│   └── pdf_generator.py       # PDF report generation
│
├── rag_pipeline/              # Medical Knowledge Base
│   ├── rag_init.py           # Initialize ChromaDB with medical data
│   └── rag_query.py          # Query medical knowledge
│
├── frontend/                  # React Dashboard
│   ├── src/
│   │   ├── App.jsx           # Main dashboard component
│   │   ├── App.css           # Dashboard styling
│   │   └── main.jsx          # React entry point
│   ├── index.html            # HTML template
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite build config
│
├── tests/                     # Testing Suite
│   ├── test_api.py           # API unit tests (5 tests)
│   └── test_scenarios.py     # Progressive test scenarios (3 scenarios)
│
├── .gitignore                # Git ignore patterns
├── LICENSE                   # MIT License
├── README.md                 # Setup instructions
└── requirements.txt          # Python dependencies
```

## Key Files

### Backend
- **main.py**: FastAPI server with `/analyze`, `/history`, `/report`, `/report/pdf` endpoints
- **risk_engine.py**: Calculates cardiac risk score from vitals + ECG parameters
- **llm_service.py**: Generates AI explanations using Llama 3.2:3b + RAG
- **database.py**: Stores all readings in SQLite for history and reports
- **pdf_generator.py**: Creates professional PDF reports with charts and ECG

### RAG Pipeline
- **rag_init.py**: Loads 6 medical documents into ChromaDB
- **rag_query.py**: Retrieves relevant medical context for AI explanations

### Frontend
- **App.jsx**: Live dashboard with ECG waveform, vitals input, risk display
- **App.css**: Dark theme styling with animations

### Tests
- **test_api.py**: 5 automated tests (normal, high risk, moderate, invalid input, root)
- **test_scenarios.py**: 3 progressive scenarios (normal → moderate → critical with 911)

## Data Flow

1. **Input**: Vitals + ECG parameters → Backend `/analyze`
2. **Processing**: Risk engine calculates score → RAG retrieves context → Llama generates explanation
3. **Storage**: Reading saved to SQLite database
4. **Output**: Risk level + explanation returned to frontend
5. **Display**: Dashboard shows live ECG waveform, risk assessment, history charts
6. **Report**: PDF generated with patient info, vitals chart, ECG, and statistics

## Running the System

See README.md for complete setup and run instructions.
