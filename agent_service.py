import os
from dotenv import load_dotenv
from llama_agents import (
    AgentService,
    AgentOrchestrator,
    ControlPlaneServer,
    ServerLauncher,
)
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere

# פתרון SSL לנטפרי
import ssl, urllib3
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# 1. הגדרת המודלים והאינדקס (הבסיס שלנו)
embed_model = CohereEmbedding(model_name="embed-multilingual-v3.0")
llm = Cohere(model="command-r-08-2024")
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context, embed_model=embed_model)

# 2. הפיכת ה-RAG לכלי (Tool) שהסוכן יכול להשתמש בו
query_engine = index.as_query_engine(llm=llm)
tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="doc_reader",
        description="משמש לקריאת החלטות טכניות וכללי פרויקט מקבצי Markdown.",
    ),
)

# 3. הגדרת רכיבי ה-LlamaAgents
# ה-Control Plane מנהל את התקשורת
control_plane = ControlPlaneServer(
    Orchestrator=AgentOrchestrator(llm=llm),
)

# הגדרת שירות הסוכן
agent_service = AgentService(
    agent=llm.as_agent(tools=[tool]),
    message_queue=None, # בשימוש פשוט לא צריך תור חיצוני
    description="סוכן שתפקידו לענות על שאלות מתוך תיעוד הפרויקט",
    service_name="project_info_agent",
)

# 4. הרצת המערכת
async def main():
    launcher = ServerLauncher(
        [agent_service],
        control_plane,
    )
    print("🚀 שירות ה-Agent עולה...")
    await launcher.launch_server()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())