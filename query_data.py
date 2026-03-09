import os
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere

# פתרון SSL לנטפרי
import ssl
import urllib3
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# טעינת המשתנים מקובץ ה-.env
load_dotenv()
api_key = os.environ.get("COHERE_API_KEY")

# בדיקה קטנה כדי לוודא שהמפתח באמת נטען
if not api_key:
    raise ValueError("❌ לא נמצא API KEY בקובץ ה-.env! ודאי שהשם שם הוא COHERE_API_KEY")

# 1. הגדרת המודלים עם העברת המפתח במפורש
embed_model = CohereEmbedding(
    model_name="embed-multilingual-v3.0",
    api_key=api_key  # הוספנו את זה כאן כדי למנוע את שגיאת ה-Validation
)

# החליפי את השורה הקיימת בשורה הזו:
llm = Cohere(
    api_key=api_key, 
    model="command-r-08-2024"  # או פשוט "command-r" לגרסה היציבה
)

# 2. טעינת האינדקס מהתיקייה המקומית
print("טוען את האינדקס מתיקיית storage...")
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context, embed_model=embed_model)

# 3. יצירת מנוע שאילתות
query_engine = index.as_query_engine(llm=llm)

# 4. שאילתה לדוגמה
question = "מה הוחלט לגבי מסד הנתונים?"
print(f"שואל: {question}")
response = query_engine.query(question)

print("\n--- תשובת המערכת ---")
print(response)