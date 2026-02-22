import chromadb
from chromadb.utils import embedding_functions

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")

# Use sentence transformers for embeddings
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Get or create collection
collection = client.get_or_create_collection(
    name="medical_knowledge",
    embedding_function=embedding_function
)

# Medical knowledge base
MEDICAL_DOCS = [
    {
        "id": "doc1",
        "text": "Normal heart rate for adults ranges from 60-100 bpm. Tachycardia (>100 bpm) may indicate stress, fever, or cardiac issues. Bradycardia (<60 bpm) can be normal in athletes but may signal heart block.",
        "metadata": {"category": "heart_rate"}
    },
    {
        "id": "doc2",
        "text": "Hypertension is defined as blood pressure ≥140/90 mmHg. Stage 2 hypertension (≥180/120) is a medical emergency requiring immediate attention. High BP increases risk of heart attack and stroke.",
        "metadata": {"category": "blood_pressure"}
    },
    {
        "id": "doc3",
        "text": "Normal oxygen saturation is 95-100%. Levels below 90% indicate hypoxemia requiring urgent intervention. Low SpO2 can result from respiratory or cardiac conditions.",
        "metadata": {"category": "oxygen"}
    },
    {
        "id": "doc4",
        "text": "Normal body temperature is 36.5-37.5°C. Fever (>38°C) may indicate infection or inflammation. Hypothermia (<36°C) can be life-threatening.",
        "metadata": {"category": "temperature"}
    },
    {
        "id": "doc5",
        "text": "Cardiac risk factors include hypertension, tachycardia, hypoxemia, and abnormal temperature. Multiple abnormal vitals significantly increase cardiovascular event risk.",
        "metadata": {"category": "cardiac_risk"}
    },
    {
        "id": "doc6",
        "text": "Critical vital signs require immediate medical attention: HR >120 or <50, BP >180/120, SpO2 <90%, or temperature >39°C or <35°C.",
        "metadata": {"category": "critical_care"}
    }
]

def initialize_knowledge_base():
    # Check if already populated
    if collection.count() > 0:
        print(f"Knowledge base already contains {collection.count()} documents")
        return
    
    # Add documents to collection
    collection.add(
        documents=[doc["text"] for doc in MEDICAL_DOCS],
        ids=[doc["id"] for doc in MEDICAL_DOCS],
        metadatas=[doc["metadata"] for doc in MEDICAL_DOCS]
    )
    print(f"Initialized knowledge base with {len(MEDICAL_DOCS)} documents")

if __name__ == "__main__":
    initialize_knowledge_base()
