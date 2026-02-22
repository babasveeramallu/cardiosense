#!/bin/bash

echo "Starting CardioSense AI..."

# Activate virtual environment
source venv/bin/activate

# Initialize RAG if needed
if [ ! -d "rag_pipeline/chroma_db" ]; then
    echo "Initializing knowledge base..."
    cd rag_pipeline
    python3 rag_init.py
    cd ..
fi

# Start backend
echo "Starting backend server..."
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
