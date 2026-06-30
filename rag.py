from datetime import date
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from vectorstore import vector_store, vector_database_result
from rss_news import get_articles
from extract import extract_article
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, max_tokens=1500)

DIGEST_PROMPT = PromptTemplate(
    template="""
    You are an AI news editor.

    Below are today's retrieved AI news articles. Each one is given as a
    Source URL followed by its content.

    context : {context}

    Task:
    - Cover as many distinct stories as the context allows (aim for 10-15
      separate items if that many distinct stories are present).
    - Combine near-duplicate coverage of the exact same story, but otherwise
      keep stories separate.
    - Produce a WhatsApp-friendly summary, 2-3 sentences per item.
    - Aim for 500-700 words total.
    - Mention company/organization names.
    - CRITICAL: end each item with the EXACT Source URL given for that
      article in the context above. Never invent, guess, or shorten a URL.
      Only use a URL that appears verbatim in the context. If an item has
      no Source URL in the context, omit the link rather than making one up.
    """,
    input_variables=["context"],
)

CHAT_PROMPT = PromptTemplate(
    template="""
    You are an AI news assistant. Answer the user's question using ONLY the
    context below, which comes from a database of recently collected AI news
    articles. Each item is given as a Source URL followed by its content.
    If the context doesn't contain relevant info, say so honestly instead of
    making things up.

    context : {context}

    question : {question}

    Keep the answer concise and WhatsApp-friendly (max ~150 words). If you
    reference a specific article, cite its EXACT Source URL from the context
    above — never invent one.
    """,
    input_variables=["context", "question"],
)


def ingest_daily_news(limit_per_feed=10):
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


def _build_context(results):
    """Join retrieved chunks, always pairing content with its real source URL."""
    parts = []
    for doc in results:
        src = doc.metadata.get("URL", "Unknown")
        parts.append(f"Source URL: {src}\nContent: {doc.page_content}")
    return "\n\n---\n\n".join(parts)


def run_daily_digest():
    query = f"{date.today().strftime('%d-%m-%Y')} AI news"
    results = vector_store.similarity_search(query=query, k=25)
    print(f"DEBUG: retrieved {len(results)} chunks from vector store")

    if not results:
        return "No AI news found for today yet."

    context = _build_context(results)
    chain = DIGEST_PROMPT | model
    response = chain.invoke({"context": context})
    return response.content


def answer_query(user_question: str):
    """Used by the webhook when a user sends a message on WhatsApp."""
    results = vector_store.similarity_search(query=user_question, k=8)

    if not results:
        return "I couldn't find anything relevant in the news database yet."

    context = _build_context(results)
    chain = CHAT_PROMPT | model
    response = chain.invoke({"context": context, "question": user_question})
    return response.content
