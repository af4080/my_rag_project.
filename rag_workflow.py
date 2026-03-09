import os
from dotenv import load_dotenv
from llama_index.core.workflow import Event, Workflow, step, StartEvent, StopEvent
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere


import ssl, urllib3
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()


class RetrievedEvent(Event):
    nodes: list
    query: str

class ValidationEvent(Event):
    context: str
    query: str


class AgenticRAGWorkflow(Workflow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.embed_model = CohereEmbedding(model_name="embed-multilingual-v3.0")
        self.llm = Cohere(model="command-r-08-2024")
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        self.index = load_index_from_storage(storage_context, embed_model=self.embed_model)

    @step
    async def retrieve(self, ev: StartEvent) -> RetrievedEvent | None:
        query = ev.get("query")
        if not query:
            print("❌ שגיאה: שאילתה ריקה")
            return None
        
        print(f"🔍 שלב 1: שולף מידע עבור: {query}")
        retriever = self.index.as_retriever(similarity_top_k=2)
        nodes = retriever.retrieve(query)
        return RetrievedEvent(nodes=nodes, query=query)

    @step
    async def validate(self, ev: RetrievedEvent) -> ValidationEvent | StopEvent:
        print("⚖️ שלב 2: ולידציה - בודק אם המידע רלוונטי...")
        

        if not ev.nodes:
            return StopEvent(result="מצטער, לא מצאתי מידע רלוונטי בקבצי התיעוד.")

        context = "\n".join([n.get_content() for n in ev.nodes])
        

        return ValidationEvent(context=context, query=ev.query)

    @step
    async def synthesize(self, ev: ValidationEvent) -> StopEvent:
        print("✍️ שלב 3: מנסח תשובה סופית...")
        prompt = f"מבוסס על המידע הבא:\n{ev.context}\n\nשאלה: {ev.query}\nתשובה:"
        response = await self.llm.acomplete(prompt)
        return StopEvent(result=str(response))

async def main():
    agent = AgenticRAGWorkflow(timeout=60, verbose=True)
    result = await agent.run(query="מה הוחלט לגבי RTL?")
    print("\n--- תוצאה סופית מה-Agent ---")
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())