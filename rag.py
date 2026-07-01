from datetime import date
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from tools import search_news_database, get_latest_headlines
from vectorstore import vector_store, vector_database_result
from rss_news import get_articles
from extract import extract_article
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, max_tokens=1500)
tools = [search_news_database, get_latest_headlines]
model_with_tools = model.bind_tools(tools)

DIGEST_PROMPT = PromptTemplate(
    template="""
    You are an AI news editor.

    Below are today's retrieved AI news articles.

    context : {context}

    Task:
Task:
- Combine similar stories.
- Remove duplicate information.
- Produce a WhatsApp-friendly summary.
- Each news item should be 50–70 words.
- For each news item explain:
  1. What happened?
  2. Why is it important?
  3. Who is involved?
- Mention the company names naturally.
- Do NOT copy the article title only.
- Explain the key update in simple language.
- End each news item with the provided Source URL exactly as given.
- Never invent or modify URLs.
- Use a short emoji in the heading.
- Leave one blank line between news items.

    """,
    input_variables=["context"],
)

def ingest_daily_news(limit_per_feed=7):
    """Scrape feeds, extract article text, embed + store in vector DB."""
    articles = get_articles(limit_per_feed=limit_per_feed)
    saved = 0

    for article in articles:
        url = article["url"]
        text = extract_article(url)
        if not text:
            continue
        vector_database_result(text, url)
        saved += 1

    return saved


def run_daily_digest():
    query = f"AI news {date.today().isoformat()}"
    results = vector_store.similarity_search(query=query, k=10)
    print(f"DEBUG: retrieved {len(results)} chunks from vector store")

    if not results:
        return "No AI news found for today yet."

    context = ""

    for doc in results:
        context += f"""
        Article:
        {doc.page_content}
        
        Source URL:
        {doc.metadata.get("URL", "Unavailable")}
        
        -------------------------
        """

    chain = DIGEST_PROMPT | model
    response = chain.invoke({"context": context})
    return response.content

def agentic_answer(user_question: str) -> str:
    messages: list[BaseMessage] = [HumanMessage(user_question)]
    
    response = model_with_tools.invoke(messages)
    messages.append(response)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_fn = {t.name: t for t in tools}[tool_call["name"]]
            tool_result = tool_fn.invoke(tool_call) 
            messages.append(tool_result)
        
        final = model_with_tools.invoke(messages)
        return final.content

    return response.content
