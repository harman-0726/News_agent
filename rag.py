from datetime import date
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from vectorstore import vector_store, vector_database_result
from rss_news import get_articles
from extract import extract_article
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

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

CHAT_PROMPT = PromptTemplate(
    template="""
    You are an AI news assistant. Answer the user's question using ONLY the
    context below, which comes from a database of recently collected AI news
    articles. If the context doesn't contain relevant info, say so honestly
    instead of making things up.

    context : {context}

    question : {question}

    Keep the answer concise and WhatsApp-friendly (max ~150 words).
    """,
    input_variables=["context", "question"],
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

def answer_query(user_question: str):
    """Used by the webhook when a user sends a message on WhatsApp."""
    results = vector_store.similarity_search(query=user_question, k=10)

    if not results:
        return "I couldn't find anything relevant in the news database yet."

    context = "\n\n".join(doc.page_content for doc in results)
    chain = CHAT_PROMPT | model
    response = chain.invoke({"context": context, "question": user_question})
    return response.content
