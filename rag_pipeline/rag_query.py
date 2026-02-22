import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./chroma_db")
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def query_medical_knowledge(vitals, risk_level):
    try:
        collection = client.get_collection(
            name="medical_knowledge",
            embedding_function=embedding_function
        )
        
        # Build query based on vitals
        query_text = f"cardiac risk {risk_level} heart rate {vitals.heart_rate} blood pressure {vitals.blood_pressure_systolic}/{vitals.blood_pressure_diastolic} oxygen {vitals.oxygen_saturation}"
        
        # Query the collection
        results = collection.query(
            query_texts=[query_text],
            n_results=3
        )
        
        # Combine retrieved documents
        context = "\n".join(results['documents'][0])
        return context
    
    except Exception as e:
        return "General cardiac monitoring guidelines apply."
