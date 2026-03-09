import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.cohere import CohereEmbedding
from pinecone import Pinecone

load_dotenv()

# 1. התחברות ל-Pinecone
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

# ודאי שיצרת אינדקס בלוח הבקרה של Pinecone עם 1024 מימדים (Dimensions)
pinecone_index = pc.Index("agentic-index") 

# 2. הגדרת מודל ה-Embedding (המתרגם של הטקסט למספרים)
embed_model = CohereEmbedding(
    model_name="embed-multilingual-v3.0", 
    api_key=os.environ["COHERE_API_KEY"]
)

# 3. טעינת המסמכים מהתיקייה שיצרנו
documents = SimpleDirectoryReader("./mock_docs").load_data()

# 4. חיבור ה-Vector Store של LlamaIndex ל-Pinecone
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 5. יצירת האינדקס ושליחה לענן
index = VectorStoreIndex.from_documents(
    documents, 
    storage_context=storage_context, 
    embed_model=embed_model
)

print("✅ המידע עלה ל-Pinecone בהצלחה!")