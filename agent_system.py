import os
import json
from dotenv import load_dotenv


from llama_index.core.agent import AgentRunner, ReActAgentWorker
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere

# פתרון SSL לנטפרי
import ssl, urllib3
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# --- 1. הגדרת המודלים והאינדקס ---
api_key = os.environ.get("COHERE_API_KEY")
embed_model = CohereEmbedding(model_name="embed-multilingual-v3.0", api_key=api_key)
llm = Cohere(model="command-r-08-2024", api_key=api_key)

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context, embed_model=embed_model)

# --- 2. הגדרת הכלים (Tools) ---

# כלי א': RAG
query_engine = index.as_query_engine(llm=llm)
rag_tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="documentation_search",
        description="שימושי לשאלות על תוכן המסמכים והסברים טכניים.",
    ),
)

# כלי ב': JSON
def get_extracted_decisions():
    try:
        with open("extracted_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"Error loading JSON: {str(e)}"

json_tool = FunctionTool.from_defaults(
    fn=get_extracted_decisions,
    name="structured_data_viewer",
    description="שימושי לנתונים כמותיים, סטטוסים וספירת החלטות.",
)

# --- 3. יצירת הסוכן באמצעות Worker (השיטה הכי חסינה לשגיאות) ---
worker = ReActAgentWorker.from_tools(
    tools=[rag_tool, json_tool],
    llm=llm,
    verbose=True
)
agent = AgentRunner(worker)

# --- 4. הרצה ---
def run_demo():
    print("\n--- שאילתה 1: נתונים מובנים ---")
    # בשיטה זו משתמשים ב-query במקום chat אם chat לא מזוהה
    response1 = agent.query("כמה החלטות מופיעות בנתונים המובנים?")
    print(f"תשובה: {response1}")

    print("\n--- שאילתה 2: הסברים טכניים ---")
    response2 = agent.query("מה הוחלט לגבי מסד הנתונים ולמה?")
    print(f"תשובה: {response2}")

if __name__ == "__main__":
    run_demo()