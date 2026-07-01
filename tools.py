from langchain_core.tools import tool
from langchain.agents import create_agent
from vectorstore import vector_store
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()

load_dotenv()

model = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0
)

@tool
def search_news_database(query: str) -> str:
    """Search the existing vector DB of already-ingested AI news articles."""
    results = vector_store.similarity_search(query=query, k=8)
    if not results:
        return "No relevant articles found in the database."
    return "\n\n---\n\n".join(
        f"Source URL: {doc.metadata.get('URL')}\nContent: {doc.page_content}"
        for doc in results
    )
  
search = DuckDuckGoSearchRun()

agent = create_agent(
    model=model,
    tools=[search_news_database, search],
    checkpointer=memory,
    system_prompt="""
You are an AI News Assistant.

Rules:

1. Use the available tools to answer factual questions.
2. Prefer the vector database. If it doesn't contain enough information, use DuckDuckGo Search automatically.
3. Never invent facts or answer from prior knowledge when tool information is needed.
4. Start directly with the answer. Do not write "Result:", "Final Answer:", or any other heading.
5. Keep the answer under 100 words unless the user asks for more detail.
6. If the user asks a follow-up question, use the previous conversation as context.
7. At the end of every response include:

Source Information
------------------
Source Type:
"""
)

def agent_answer(query):
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        },
        config={
        "configurable": {
            "thread_id": "harmandeep_chat_1"
        }
    }
    )

    return response["messages"][-1].content
