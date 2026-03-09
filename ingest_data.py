import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.embeddings.cohere import CohereEmbedding

# פתרון לנטפרי (SSL)
import ssl
import urllib3
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# 1. הגדרת מודל ה-Embedding של Cohere
embed_model = CohereEmbedding(
    model_name="embed-multilingual-v3.0", 
    api_key=os.environ["COHERE_API_KEY"]
)

# 2. טעינת המסמכים מהתיקייה
print("טוען מסמכים...")
documents = SimpleDirectoryReader("./mock_docs").load_data()

# 3. יצירת האינדקס בזיכרון (In-memory)
print("יוצר אינדקס וקטורי (זה עשוי לקחת כמה שניות)...")
index = VectorStoreIndex.from_documents(
    documents, 
    embed_model=embed_model
)

# 4. שמירה פיזית לתיקייה מקומית בשם 'storage'
# זה מחליף את Pinecone ושומר קבצי JSON במקום
index.storage_context.persist(persist_dir="./storage")

print("✅ המידע אונדקס ונשמר בהצלחה בתיקיית ./storage!")